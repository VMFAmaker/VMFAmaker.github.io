import { mkdir, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { sections, projects, profile } from "../assets/js/content.mjs";

const root = dirname(dirname(fileURLToPath(import.meta.url)));

function html({ title, description, route, routeId = "" }) {
  return `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="${description}">
    <title>${title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/assets/css/styles.css">
  </head>
  <body data-route="${route}" data-route-id="${routeId}">
    <div class="layout">
      <aside class="sidebar" data-sidebar></aside>
      <div class="content">
        <header class="topbar">
          <button class="sidebar-toggle" data-sidebar-toggle aria-label="Open navigation">
            <span></span><span></span><span></span>
          </button>
          <span class="topbar-title">${profile.name}</span>
          <nav class="breadcrumb" data-breadcrumb></nav>
        </header>
        <main data-app></main>
        <footer class="footer">
          <span>&copy; <span data-current-year></span> ${profile.name}. Portfolio.</span>
        </footer>
      </div>
    </div>
    <script type="module" src="/assets/js/app.mjs"></script>
  </body>
</html>
`;
}

async function writePage(path, page) {
  const target = join(root, path);
  await mkdir(dirname(target), { recursive: true });
  await writeFile(target, html(page), "utf8");
}

const description = "Portfolio and projects by Virgilio MF Almeida.";

const pages = [
  ["index.html", { title: `${profile.name} | Portfolio`, description, route: "home" }],
  ["about/index.html", { title: `About | ${profile.name}`, description: "About Virgilio MF Almeida.", route: "about" }],
  ["work/index.html", { title: `Work | ${profile.name}`, description: "Projects and capability areas.", route: "work" }],
  ["contact/index.html", { title: `Contact | ${profile.name}`, description: "Get in touch with Virgilio MF Almeida.", route: "contact" }],
];

for (const project of projects) {
  pages.push([
    `work/${project.id}/index.html`,
    {
      title: `${project.title} | ${profile.name}`,
      description: project.summary,
      route: "work-detail",
      routeId: project.id,
    },
  ]);
}

await Promise.all(pages.map(([path, page]) => writePage(path, page)));
console.log(`Generated ${pages.length} pages.`);
