import { createReadStream } from "node:fs";
import { stat } from "node:fs/promises";
import { extname, join, normalize } from "node:path";
import { fileURLToPath } from "node:url";
import { createServer } from "node:http";

const root = fileURLToPath(new URL(".", import.meta.url));
const port = Number(process.env.PORT || 9004);

const contentTypes = {
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".pdf": "application/pdf",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
  ".csv": "text/csv; charset=utf-8",
};

function resolvePath(urlPath) {
  const decodedPath = decodeURIComponent(urlPath.split("?")[0]);
  const cleanPath = normalize(decodedPath).replace(/^(\.\.[/\\])+/, "");
  return join(root, cleanPath === "/" ? "index.html" : cleanPath);
}

async function getFilePath(urlPath) {
  let filePath = resolvePath(urlPath);
  const fileStat = await stat(filePath).catch(() => null);

  if (fileStat?.isDirectory()) {
    filePath = join(filePath, "index.html");
  }

  return filePath;
}

const server = createServer(async (request, response) => {
  try {
    const filePath = await getFilePath(request.url || "/");
    const fileStat = await stat(filePath).catch(() => null);

    if (!fileStat?.isFile()) {
      response.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
      response.end("Not found");
      return;
    }

    response.writeHead(200, {
      "Content-Type": contentTypes[extname(filePath)] || "application/octet-stream",
    });
    createReadStream(filePath).pipe(response);
  } catch (error) {
    response.writeHead(500, { "Content-Type": "text/plain; charset=utf-8" });
    response.end(`Server error: ${error.message}`);
  }
});

server.listen(port, () => {
  console.log(`Portfolio website running at http://localhost:${port}`);
});

