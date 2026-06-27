import { readFile, writeFile, readdir, stat } from "node:fs/promises";
import { join, extname, dirname, basename } from "node:path";
import { fileURLToPath } from "node:url";
import { execSync } from "node:child_process";
import { getDocument } from "pdfjs-dist/legacy/build/pdf.mjs";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const pdfDir = join(root, "pdf");
const syncPath = join(root, "assets", "js", "projects-sync.mjs");
const contentPath = join(root, "assets", "js", "content.mjs");

function getGitHubToken() {
  return execSync("gh auth token", { encoding: "utf8" }).trim();
}

async function extractText(pdfPath, maxPages = 5) {
  const data = new Uint8Array(await readFile(pdfPath));
  const doc = await getDocument({ data, useSystemFonts: true }).promise;
  const pages = Math.min(doc.numPages, maxPages);
  const lines = [];
  for (let i = 1; i <= pages; i++) {
    const page = await doc.getPage(i);
    const content = await page.getTextContent();
    lines.push(content.items.map((item) => item.str).join(" "));
  }
  return lines.join("\n").slice(0, 4000);
}

async function findPdfs(dir) {
  const results = [];
  try {
    const entries = await readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      const full = join(dir, entry.name);
      if (entry.isDirectory()) results.push(...(await findPdfs(full)));
      else if (extname(entry.name).toLowerCase() === ".pdf") results.push(full);
    }
  } catch {}
  return results;
}

async function callGitHubModels(token, prompt) {
  const res = await fetch("https://models.inference.ai.azure.com/chat/completions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "gpt-4o-mini",
      messages: [
        {
          role: "system",
          content:
            "You generate structured JSON descriptions for portfolio projects. Be concise and professional. Return ONLY valid JSON, no markdown fences.",
        },
        { role: "user", content: prompt },
      ],
      temperature: 0.3,
      max_tokens: 800,
    }),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`GitHub Models API ${res.status}: ${err}`);
  }

  const data = await res.json();
  return data.choices[0].message.content.trim();
}

async function generateForProject(project, token) {
  const projectPdfDir = join(pdfDir, project.roleId, project.id);
  const pdfs = await findPdfs(projectPdfDir);

  if (pdfs.length === 0) return null;

  let combinedText = "";
  for (const pdf of pdfs.slice(0, 3)) {
    const text = await extractText(pdf);
    combinedText += `\n--- ${basename(pdf)} ---\n${text}`;
  }

  if (combinedText.length < 50) return null;

  const prompt = `You are writing portfolio descriptions for a professional BBA student's website. Read the document content carefully and write descriptions that reference SPECIFIC details from the actual work — names, figures, frameworks, industries, findings. NEVER write generic filler like "actionable recommendations for improving operational efficiency" or "set within the context of a competitive market." If the document mentions a company, name it. If it mentions a margin figure, quote it. If it uses a framework, say which one.

Use British English throughout (analyse, organised, colour, labour, etc.).

Generate a JSON object with these fields:
- "summary": 2-3 sentences. What this project IS, what industry/company/topic it covers, and what it delivers. Be specific — mention the actual subject, not "a company" or "a business."
- "objective": 2 sentences. What the project set out to achieve and why. Reference the actual problem or question from the document.
- "context": 2-3 sentences. The real-world backdrop — what industry pressures, academic debates, or business situations motivated this work. Pull specific details from the document (market conditions, regulatory issues, competitive dynamics, etc.).
- "approach": 2 sentences. What methods, frameworks, or tools were actually used. Name them (SWOT, DCF, Porter's Five Forces, Monte Carlo, etc.).
- "result": 2 sentences. What was actually produced or concluded. If there are specific findings, recommendations, or figures, mention them. Do NOT say "actionable recommendations" without saying what they recommend.
- "skills": array of exactly 7 specific professional skills demonstrated in this work

Project title: "${project.title}"
Role category: "${project.roleId}"

Document content (excerpts):
${combinedText.slice(0, 3500)}

Return ONLY the JSON object, no markdown fences.`;

  const raw = await callGitHubModels(token, prompt);
  const cleaned = raw.replace(/^```json?\s*/i, "").replace(/\s*```$/i, "");
  return JSON.parse(cleaned);
}

async function main() {
  const token = getGitHubToken();
  console.log("GitHub token obtained.\n");

  const module = await import("../assets/js/projects-sync.mjs");
  const projects = module.default || [];

  if (projects.length === 0) {
    console.log("No synced projects found. Run sync.mjs first.");
    return;
  }

  const forceAll = process.argv.includes("--force");
  console.log(`Processing ${projects.length} synced projects...${forceAll ? " (force regenerate all)" : ""}\n`);

  let updated = 0;
  const updatedProjects = [];

  for (const project of projects) {
    const needsDescription =
      forceAll ||
      project.summary === "Project documents available — summary will be added." ||
      !project.skills ||
      project.skills.length === 0;

    if (!needsDescription) {
      console.log(`  SKIP  ${project.title} (already has description)`);
      updatedProjects.push(project);
      continue;
    }

    process.stdout.write(`  AI  ${project.title} ... `);
    try {
      if (updated > 0) await new Promise((r) => setTimeout(r, 4500));
      const generated = await generateForProject(project, token);
      if (generated) {
        updatedProjects.push({
          ...project,
          summary: generated.summary || project.summary,
          objective: generated.objective || project.objective,
          context: generated.context || project.context,
          approach: generated.approach || project.approach,
          result: generated.result || project.result,
          skills: generated.skills || project.skills,
        });
        console.log("OK");
        updated++;
      } else {
        console.log("SKIP (no PDF content)");
        updatedProjects.push(project);
      }
    } catch (err) {
      console.log(`FAIL: ${err.message}`);
      updatedProjects.push(project);
    }
  }

  const code = `// Auto-generated by tools/sync.mjs — do not edit manually\nexport default ${JSON.stringify(updatedProjects, null, 2)};\n`;
  await writeFile(syncPath, code, "utf8");
  console.log(`\nUpdated ${updated} project descriptions.`);
  console.log(`Wrote ${updatedProjects.length} projects to projects-sync.mjs`);
}

main().catch((err) => {
  console.error("Description generation failed:", err);
  process.exit(1);
});
