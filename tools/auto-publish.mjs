import { execSync } from "node:child_process";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(dirname(fileURLToPath(import.meta.url)));

function run(cmd, label) {
  console.log(`\n${"=".repeat(50)}`);
  console.log(`  ${label}`);
  console.log("=".repeat(50));
  execSync(cmd, { cwd: root, stdio: "inherit", timeout: 600_000 });
}

async function main() {
  console.log("VMFA Portfolio — Auto Publish");
  console.log(`Started: ${new Date().toISOString()}\n`);

  // 1. Sync files from Portfolio folder
  run("node tools/sync.mjs", "SYNC — Scanning Portfolio folder");

  // 2. Convert Office files to watermarked PDFs
  run("node tools/build-pdfs.mjs", "BUILD PDFS — Converting documents");

  // 3. Generate AI descriptions for new projects
  run("node tools/generate-descriptions.mjs", "AI DESCRIPTIONS — Generating content");

  // 4. Regenerate static HTML pages
  run("node tools/generate-pages.mjs", "PAGES — Regenerating HTML");

  // 5. Git commit and push (only if there are changes)
  console.log(`\n${"=".repeat(50)}`);
  console.log("  GIT — Commit and push");
  console.log("=".repeat(50));

  try {
    const status = execSync("git status --porcelain", { cwd: root, encoding: "utf8" });
    if (!status.trim()) {
      console.log("No changes to commit. Site is up to date.");
      return;
    }

    execSync("git add -A", { cwd: root, stdio: "inherit" });

    const date = new Date().toISOString().slice(0, 10);
    const msg = `Auto-publish ${date} — sync, convert, and update portfolio`;
    execSync(`git commit -m "${msg}"`, { cwd: root, stdio: "inherit" });
    execSync("git push origin master", { cwd: root, stdio: "inherit" });
    console.log("\nPushed to GitHub. Site will update shortly.");
  } catch (err) {
    console.error("Git operation failed:", err.message);
  }

  console.log(`\nFinished: ${new Date().toISOString()}`);
}

main().catch((err) => {
  console.error("Auto-publish failed:", err);
  process.exit(1);
});
