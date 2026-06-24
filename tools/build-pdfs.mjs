import { execSync } from "node:child_process";
import { readdir, stat, mkdir, readFile, writeFile, unlink } from "node:fs/promises";
import { join, extname, basename, dirname, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { tmpdir } from "node:os";
import { PDFDocument, rgb, degrees, StandardFonts } from "pdf-lib";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const filesDir = join(root, "files");
const pdfDir = join(root, "pdf");

const OFFICE_EXTS = new Set([".docx", ".xlsx", ".pptx"]);
const WATERMARK_TEXT = "VA";
const WATERMARK_OPACITY = 0.07;
const WATERMARK_SIZE = 120;
const WATERMARK_ROTATION = 45;

async function findOfficeFiles(dir) {
  const results = [];
  const entries = await readdir(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...(await findOfficeFiles(full)));
    } else if (OFFICE_EXTS.has(extname(entry.name).toLowerCase())) {
      results.push(full);
    }
  }
  return results;
}

async function convertWithOffice(srcPath, outDir) {
  const ext = extname(srcPath).toLowerCase();
  const pdfName = basename(srcPath, ext) + ".pdf";
  const outPath = join(outDir, pdfName);

  let app, formatId;
  if (ext === ".docx") {
    app = "Word";
    formatId = 17; // wdFormatPDF
  } else if (ext === ".xlsx") {
    app = "Excel";
    formatId = 0; // xlTypePDF
  } else if (ext === ".pptx") {
    app = "PowerPoint";
    formatId = 32; // ppSaveAsPDF
  }

  let script;
  if (app === "Word") {
    script = `
$src = '${srcPath.replaceAll("'", "''")}'
$out = '${outPath.replaceAll("'", "''")}'
$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
try {
  $doc = $w.Documents.Open($src, $false, $true)
  $doc.SaveAs([ref]$out, [ref]${formatId})
  $doc.Close($false)
} finally { $w.Quit() }
`;
  } else if (app === "Excel") {
    script = `
$src = '${srcPath.replaceAll("'", "''")}'
$out = '${outPath.replaceAll("'", "''")}'
$e = New-Object -ComObject Excel.Application
$e.Visible = $false
$e.DisplayAlerts = $false
try {
  $wb = $e.Workbooks.Open($src, 0, $true)
  $wb.ExportAsFixedFormat(${formatId}, $out)
  $wb.Close($false)
} finally { $e.Quit() }
`;
  } else if (app === "PowerPoint") {
    script = `
$src = '${srcPath.replaceAll("'", "''")}'
$out = '${outPath.replaceAll("'", "''")}'
$p = New-Object -ComObject PowerPoint.Application
try {
  $pres = $p.Presentations.Open($src, $true, $false, $false)
  $pres.SaveAs($out, ${formatId})
  $pres.Close()
} finally { $p.Quit() }
`;
  }

  const tmpScript = join(tmpdir(), `convert-${Date.now()}.ps1`);
  await writeFile(tmpScript, script, "utf8");
  try {
    execSync(`powershell -NonInteractive -ExecutionPolicy Bypass -File "${tmpScript}"`, {
      timeout: 120_000,
      stdio: "pipe",
    });
  } finally {
    await unlink(tmpScript).catch(() => {});
  }

  return outPath;
}

async function watermarkPdf(pdfPath) {
  const bytes = await readFile(pdfPath);
  const doc = await PDFDocument.load(bytes);
  const font = await doc.embedFont(StandardFonts.HelveticaBold);
  const pages = doc.getPages();

  for (const page of pages) {
    const { width, height } = page.getSize();
    const textWidth = font.widthOfTextAtSize(WATERMARK_TEXT, WATERMARK_SIZE);
    const textHeight = WATERMARK_SIZE;

    const spacingX = textWidth + 140;
    const spacingY = textHeight + 180;

    for (let y = -height; y < height * 2; y += spacingY) {
      for (let x = -width; x < width * 2; x += spacingX) {
        page.drawText(WATERMARK_TEXT, {
          x,
          y,
          size: WATERMARK_SIZE,
          font,
          color: rgb(0.5, 0.5, 0.5),
          opacity: WATERMARK_OPACITY,
          rotate: degrees(WATERMARK_ROTATION),
        });
      }
    }
  }

  const watermarked = await doc.save();
  await writeFile(pdfPath, watermarked);
}

async function main() {
  const files = await findOfficeFiles(filesDir);
  console.log(`Found ${files.length} Office files to convert.\n`);

  let converted = 0;
  let failed = 0;

  for (const file of files) {
    const rel = relative(filesDir, file);
    const ext = extname(file).toLowerCase();
    const outSubDir = join(pdfDir, dirname(rel));
    await mkdir(outSubDir, { recursive: true });

    const pdfName = basename(file, ext) + ".pdf";
    const outPath = join(outSubDir, pdfName);

    try {
      const outStat = await stat(outPath).catch(() => null);
      const srcStat = await stat(file);
      if (outStat && outStat.mtimeMs >= srcStat.mtimeMs) {
        console.log(`  SKIP  ${rel} (up to date)`);
        converted++;
        continue;
      }

      process.stdout.write(`  CONVERT  ${rel} ... `);
      await convertWithOffice(file, outSubDir);
      console.log("OK");

      process.stdout.write(`  WATERMARK  ${pdfName} ... `);
      await watermarkPdf(outPath);
      console.log("OK");

      converted++;
    } catch (err) {
      console.log(`FAIL: ${err.message}`);
      failed++;
    }
  }

  console.log(`\nDone: ${converted} converted, ${failed} failed.`);
}

main();
