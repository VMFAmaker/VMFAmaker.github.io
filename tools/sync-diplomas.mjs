// Scans Portfolio/Diplomas, renders each certificate to a web image, and writes
// assets/js/diplomas-sync.mjs for the Diplomas page.
//
// Accepts PDFs (first page rendered) and images (.png .jpg .jpeg .webp).
// Rendering uses Python with PyMuPDF (PDFs) and Pillow (images).

import { readFile, readdir, stat, mkdir, rm, writeFile, copyFile } from "node:fs/promises";
import { execFileSync } from "node:child_process";
import { dirname, extname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const config = JSON.parse(await readFile(join(root, "tools", "folder-map.json"), "utf8"));
const sourceDir = resolve(config.portfolioPath, config.diplomasPath || "Diplomas");
const outDir = join(root, "diplomas", "img");
const webBase = "/diplomas/img";
const dataPath = join(root, "assets", "js", "diplomas-sync.mjs");

const PDF_EXTS = new Set([".pdf"]);
const IMAGE_EXTS = new Set([".png", ".jpg", ".jpeg", ".webp"]);

const RENDER_PY = String.raw`
import json, re, sys
src, kind, full_out, thumb_out = sys.argv[1:5]
meta = {"title": "", "verify": ""}
if kind == "pdf":
    import fitz
    doc = fitz.open(src)
    page = doc[0]
    page.get_pixmap(dpi=150).save(full_out, jpg_quality=88)
    page.get_pixmap(dpi=36).save(thumb_out, jpg_quality=80)
    meta["title"] = (doc.metadata or {}).get("title") or ""
    text = " ".join(page.get_text().split())
    m = re.search(r"https?://\S+", text)
    if m:
        meta["verify"] = m.group(0).rstrip(".,)")
else:
    from PIL import Image, ImageOps
    img = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    full = img.copy()
    full.thumbnail((1800, 1800))
    full.save(full_out, "JPEG", quality=88)
    thumb = img.copy()
    thumb.thumbnail((360, 360))
    thumb.save(thumb_out, "JPEG", quality=80)
print(json.dumps(meta))
`;

function slugify(name) {
  return name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

function titleFromFilename(name) {
  const base = name.replace(/\.[^.]+$/, "").replace(/[-_]+/g, " ").trim();
  return base.charAt(0).toUpperCase() + base.slice(1);
}

// "AI capabilities and limitations: Claude Academy completion badge"
//   -> { title: "AI capabilities and limitations", issuer: "Claude Academy" }
function splitPdfTitle(raw) {
  const parts = raw.split(/:\s+/);
  if (parts.length < 2) return { title: raw.trim(), issuer: "" };
  const tail = parts.pop();
  const issuer = tail.replace(/\b(completion\s+)?(badge|certificate|diploma)\b/gi, "").trim();
  return { title: parts.join(": ").trim(), issuer };
}

async function listSources(dir) {
  const found = [];
  let entries = [];
  try {
    entries = await readdir(dir, { withFileTypes: true });
  } catch {
    return found;
  }
  for (const entry of entries) {
    if (entry.name.startsWith(".") || entry.name.toLowerCase() === "desktop.ini") continue;
    const full = join(dir, entry.name);
    if (entry.isDirectory()) {
      found.push(...(await listSources(full)));
      continue;
    }
    const ext = extname(entry.name).toLowerCase();
    if (PDF_EXTS.has(ext) || IMAGE_EXTS.has(ext)) {
      found.push({ name: entry.name, path: full, ext, mtime: (await stat(full)).mtimeMs });
    }
  }
  return found;
}

function render(src, kind, fullOut, thumbOut) {
  const output = execFileSync("python", ["-c", RENDER_PY, src, kind, fullOut, thumbOut], {
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
    env: { ...process.env, PYTHONIOENCODING: "utf-8", PYTHONWARNINGS: "ignore" },
  });
  const lastLine = output.trim().split(/\r?\n/).pop();
  return JSON.parse(lastLine);
}

async function run() {
  console.log(`Scanning ${sourceDir}...`);
  const sources = (await listSources(sourceDir)).sort((a, b) => b.mtime - a.mtime);

  await rm(outDir, { recursive: true, force: true });
  await mkdir(outDir, { recursive: true });

  const diplomas = [];
  const usedIds = new Set();

  for (const source of sources) {
    let id = slugify(source.name.replace(/\.[^.]+$/, "")) || "diploma";
    while (usedIds.has(id)) id += "-2";
    usedIds.add(id);

    const isPdf = PDF_EXTS.has(source.ext);
    const image = `${webBase}/${id}.jpg`;
    const thumb = `${webBase}/${id}-thumb.jpg`;

    try {
      const meta = render(source.path, isPdf ? "pdf" : "image", join(outDir, `${id}.jpg`), join(outDir, `${id}-thumb.jpg`));
      const named = meta.title ? splitPdfTitle(meta.title) : { title: titleFromFilename(source.name), issuer: "" };

      let pdf = "";
      if (isPdf) {
        await copyFile(source.path, join(outDir, `${id}.pdf`));
        pdf = `${webBase}/${id}.pdf`;
      }

      diplomas.push({ id, title: named.title, issuer: named.issuer, image, thumb, pdf, verify: meta.verify || "" });
      console.log(`  OK    ${source.name}`);
    } catch (err) {
      console.log(`  FAIL  ${source.name}: ${(err.stderr || err.message || "").toString().trim().split(/\r?\n/).pop()}`);
    }
  }

  const code = `// Auto-generated by tools/sync-diplomas.mjs — do not edit manually\nexport default ${JSON.stringify(diplomas, null, 2)};\n`;
  await writeFile(dataPath, code, "utf8");
  console.log(`Wrote ${diplomas.length} diploma(s) to diplomas-sync.mjs`);
}

run().catch((err) => {
  console.error("Diploma sync failed:", err);
  process.exit(1);
});
