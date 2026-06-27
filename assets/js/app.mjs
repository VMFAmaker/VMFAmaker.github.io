import {
  sections,
  roles,
  getSection,
  getRole,
  getRolesBySection,
  getProject,
  getProjectsByRole,
  getProjectsBySection,
  getSectionForProject,
  profile,
  projects,
  statusStyles,
  thinkingEntries,
  scriptures,
} from "./content.mjs";

const route = document.body.dataset.route || "home";
const routeId = document.body.dataset.routeId || "";
const app = document.querySelector("[data-app]");

const HIDDEN_STATUSES = new Set(["Draft", "Planned"]);
const visibleProjects = projects.filter((p) => !HIDDEN_STATUSES.has(p.status));

function getVisibleProjectsByRole(roleId) {
  return visibleProjects.filter((p) => p.roleId === roleId);
}

function getVisibleProjectsBySection(sectionId) {
  const sectionRoleIds = getRolesBySection(sectionId).map((r) => r.id);
  return visibleProjects.filter((p) => sectionRoleIds.includes(p.roleId));
}

const crossSvg = (size = 14) => `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="12" y1="2" x2="12" y2="22"/><line x1="5" y1="9" x2="19" y2="9"/></svg>`;

function scriptureBlock(key) {
  const s = scriptures[key];
  if (!s) return "";
  return `
    <div class="scripture-block">
      <span class="scripture-cross">${crossSvg(14)}</span>
      <span class="scripture-verse">“${escapeHtml(s.verse)}”</span>
      <span class="scripture-ref">${escapeHtml(s.reference)}</span>
    </div>
  `;
}

function crossDivider() {
  return `<div class="cross-divider">${crossSvg(14)}</div>`;
}


function projectPath(project) {
  return `/work/${project.id}/`;
}

const OFFICE_EXTS = [".docx", ".xlsx", ".pptx"];

function fileToPdfPath(filePath) {
  const ext = filePath.match(/\.\w+$/)?.[0]?.toLowerCase();
  if (!ext || !OFFICE_EXTS.includes(ext)) return null;
  const withoutFiles = filePath.replace(/^\/files\//, "");
  const pdfName = withoutFiles.replace(/\.\w+$/, ".pdf");
  return `/pdf/${pdfName}`;
}

function viewerUrl(file, projectId) {
  const pdfPath = fileToPdfPath(file.path);
  if (!pdfPath) return null;
  const params = new URLSearchParams({
    file: pdfPath,
    title: file.label,
    back: `/work/${projectId}/`,
  });
  return `/view/?${params}`;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function statusPill(status) {
  const style = statusStyles[status] || statusStyles.Planned;
  return `
    <span class="status-pill" style="--status-color: ${style.color}">
      <span class="status-dot"></span>
      ${escapeHtml(style.label)}
    </span>
  `;
}

function tags(items) {
  if (!items?.length) return "";
  return `<div class="tag-list">${items.map((item) => `<span>${escapeHtml(item)}</span>`).join("")}</div>`;
}

function renderBreadcrumb() {
  const el = document.querySelector("[data-breadcrumb]");
  if (!el) return;

  const crumbs = {
    home: [],
    about: [{ label: "About" }],
    work: [{ label: "Work" }],
    "work-detail": (() => {
      const project = getProject(routeId);
      if (!project) return [{ label: "Work", href: "/work/" }, { label: "Unknown" }];
      return [{ label: "Work", href: "/work/" }, { label: project.title }];
    })(),
    contact: [{ label: "Contact" }],
  };

  const trail = crumbs[route] || [];
  el.innerHTML = trail
    .map((c, i) => {
      const sep = i > 0 ? `<span class="sep">/</span>` : "";
      const link = c.href ? `<a href="${c.href}">${escapeHtml(c.label)}</a>` : `<span>${escapeHtml(c.label)}</span>`;
      return sep + link;
    })
    .join("");
}

function renderSidebar() {
  const sidebars = document.querySelectorAll("[data-sidebar]");

  const html = `
    <div class="brand-block">
      <a href="/" class="brand-mark" aria-label="Home"><img src="/assets/img/va-logo.png" alt="VA"></a>
      <button class="sidebar-toggle" data-sidebar-toggle aria-label="Toggle navigation">
        <span></span><span></span><span></span>
      </button>
    </div>
    <nav class="site-nav" aria-label="Primary">
      <a class="${route === "home" ? "is-active" : ""}" href="/">Home</a>
      <a class="${route === "about" ? "is-active" : ""}" href="/about/">About</a>
      <a class="${route === "work" || route === "work-detail" ? "is-active" : ""}" href="/work/">Work</a>
      <a class="${route === "contact" ? "is-active" : ""}" href="/contact/">Contact</a>
    </nav>
    <div class="sidebar-note">
      <span>Portfolio</span>
      <strong>${visibleProjects.length} projects across ${sections.length} areas</strong>
    </div>
  `;

  sidebars.forEach((sidebar) => {
    sidebar.innerHTML = html;
  });
}

function bindNavigation() {
  document.addEventListener("click", (event) => {
    const toggle = event.target.closest("[data-sidebar-toggle]");
    if (!toggle) return;
    document.body.classList.toggle("nav-open");
  });
}

function shell(content) {
  return `<section class="page-shell">${content}</section>`;
}

function introKicker(label) {
  return `<p class="kicker">${escapeHtml(label)}</p>`;
}

function projectCard(project) {
  const role = getRole(project.roleId);
  const section = role ? getSection(role.sectionId) : sections[0];

  return `
    <a class="project-card" href="${projectPath(project)}" data-section="${section.id}" data-role="${role?.id || ""}" style="--area-color: ${section.accent}">
      <div class="project-card-top">
        <span class="project-area">${escapeHtml(role?.title || "")}</span>
        ${statusPill(project.status)}
      </div>
      <div>
        <h3>${escapeHtml(project.title)}</h3>
        <p>${escapeHtml(project.summary)}</p>
      </div>
      <div class="project-card-bottom">
        <span>${escapeHtml(project.date)}</span>
        <span>Open project</span>
      </div>
    </a>
  `;
}

function sectionCard(section) {
  const sectionProjects = getVisibleProjectsBySection(section.id);
  const sectionRoles = getRolesBySection(section.id);
  return `
    <a class="area-card" href="/work/" data-filter-section="${section.id}" style="--area-color: ${section.accent}">
      <h3>${escapeHtml(section.title)}</h3>
      <p>${escapeHtml(section.summary)}</p>
      <span class="area-meta">${sectionRoles.length} roles &middot; ${sectionProjects.length} projects</span>
    </a>
  `;
}

function renderHome() {
  return shell(`
    <div class="hero-grid">
      <div class="hero-copy">
        ${introKicker("Portfolio")}
        <h1>${escapeHtml(profile.name)}</h1>
        <p class="hero-subtitle">${escapeHtml(profile.role)}</p>
        <div class="hero-actions">
          <a class="button primary" href="/work/">View work</a>
          <a class="button secondary" href="/about/">About me</a>
        </div>
      </div>
      <div class="system-panel hero-panel">
        <div class="panel-header">
          <span>Portfolio Areas</span>
          <strong>${sections.length} sections</strong>
        </div>
        <div class="signal-grid">
          ${sections.map((s) => `<a href="/work/" style="--area-color: ${s.accent}"><span>${escapeHtml(s.title)}</span></a>`).join("")}
        </div>
      </div>
    </div>

    ${scriptureBlock("home-top")}

    <section class="section-grid two">
      <div>
        ${introKicker("Why?")}
      </div>
      <div class="prose-block">
        <p>
          Work speaks where words fall short. This portfolio exists not to impress, but to show — clearly and honestly — what has been done, how it was done, and what was learnt in the process.
        </p>
        <p>
          The obstacle is the way. Every project here began with a problem that demanded thought, discipline, and execution. The purpose is not comfort but growth — to build real skill through real work, and to let the evidence stand on its own.
        </p>
      </div>
    </section>

    ${crossDivider()}

    ${visibleProjects.length > 0 ? `
    <div class="project-grid">${visibleProjects.slice(0, 4).map(projectCard).join("")}</div>
    ` : ""}

    ${scriptureBlock("home-bottom")}
  `);
}

function renderAbout() {
  return shell(`
    <div class="page-header">
      ${introKicker("About")}
      <p>
        Virgilio MF Almeida is a BBA student at SP Jain London, graduating in 2028. Driven by faith and a desire to serve,
        he seeks to use his skills in business, finance, and strategy as tools for aid — working to show Christ through
        honest effort, disciplined thinking, and care for others.
      </p>
    </div>

    <div class="info-grid">
      <article class="info-card">
        <h2>Qualifications</h2>
        ${profile.qualifications.map((q) => `
          <div class="qual-entry">
            <strong>${escapeHtml(q.title)}</strong>
            <span>${escapeHtml(q.institution)} — ${escapeHtml(q.period)}</span>
            ${q.grades ? `<span class="qual-grades">${escapeHtml(q.grades)}</span>` : ""}
          </div>
        `).join("")}
      </article>
      <article class="info-card">
        <h2>Languages</h2>
        <div class="lang-list">
          ${profile.languages.map((l) => `<div class="lang-entry"><span>${escapeHtml(l.name)}</span><span class="lang-level">${escapeHtml(l.level)}</span></div>`).join("")}
        </div>
      </article>
      <article class="info-card info-card-wide">
        <h2>Experience</h2>
        <div class="exp-list">
          ${profile.experience.map((e) => `
            <div class="exp-entry">
              <div class="exp-top">
                <strong>${escapeHtml(e.role)}</strong>${e.type ? `<span class="exp-type">${escapeHtml(e.type)}</span>` : ""}
              </div>
              <span class="exp-detail">${escapeHtml(e.company)} — ${escapeHtml(e.location)}</span>
              <span class="exp-period">${escapeHtml(e.period)}</span>
            </div>
          `).join("")}
        </div>
      </article>
      <article class="info-card info-card-wide">
        <h2>Philosophy</h2>
        <p>I test the water before I dive — but I always put the first foot in. What looks like caution is discipline. What looks like confidence is preparation meeting conviction. Once I am in, I do not come up for air until the work is done.</p>
        <p>You see what I let you see. Sociable, yes — energetic, even reckless at first glance. But beneath it, quiet, measured, and deliberate. I choose openness because I can, not because I must. The surface invites; the depth delivers.</p>
        <p>I do not work for money. I work for value — real, tangible, earned. A contract without substance is just paper. If my work carries weight, I expect it to be recognised. If yours does not, no document will make it so. We should return to a time when work spoke for itself.</p>
        <p>You do not hire a profession when you hire me. You hire a person — with creativity, convictions, and limits I am not ashamed of. If I cannot deliver, I will tell you before you find out. Christ comes first, then family, then the craft. This order is not a weakness; it is the foundation everything else stands on.</p>
        <p>I have been underestimated more times than I can count. Each time, I became more than what was expected — sometimes to prove a point, sometimes for the quiet satisfaction of it. History is not written by those who stayed where others placed them.</p>
        <p>This portfolio is not decoration. It is evidence.</p>
      </article>
    </div>
  `);
}

function renderWork() {
  const filterChips = sections
    .filter((s) => getVisibleProjectsBySection(s.id).length > 0)
    .map(
      (s) => `
        <button class="filter-chip" data-filter="${s.id}" style="--chip-color: ${s.accent}">
          ${escapeHtml(s.title)}
        </button>
      `,
    )
    .join("");

  /* Render projects grouped by section, then by role */
  const groupedContent = sections.map((section) => {
    const sectionRoles = getRolesBySection(section.id);
    const sectionProjectCount = getVisibleProjectsBySection(section.id).length;
    if (sectionProjectCount === 0) return "";

    const roleBlocks = sectionRoles.map((role) => {
      const roleProjects = getVisibleProjectsByRole(role.id);
      if (roleProjects.length === 0) return "";
      return `
        <details class="role-block" data-section="${section.id}">
          <summary class="role-header" style="--area-color: ${section.accent}">
            <h3>${escapeHtml(role.title)}</h3>
            <span class="role-toggle-meta">${roleProjects.length} project${roleProjects.length !== 1 ? "s" : ""}</span>
          </summary>
          <div class="project-grid">${roleProjects.map(projectCard).join("")}</div>
        </details>
      `;
    }).filter(Boolean).join("");

    const sectionScripture = scriptures[section.id] ? scriptureBlock(section.id) : "";

    return `
      <details class="section-block" data-section-group="${section.id}">
        <summary class="section-block-header" style="--area-color: ${section.accent}">
          <div class="section-summary-content">
            <h2>${escapeHtml(section.title)}</h2>
            <p>${escapeHtml(section.summary)}</p>
          </div>
          <span class="section-toggle-meta">${sectionProjectCount} project${sectionProjectCount !== 1 ? "s" : ""}</span>
        </summary>
        ${sectionScripture}
        ${roleBlocks}
      </details>
    `;
  }).filter(Boolean).join("");

  return shell(`
    <div class="page-header">
      ${introKicker("Work")}
      <h1>Projects by area and role</h1>
      <p>
        Each section represents an area of professional development. Within each, projects are grouped by the type of role they demonstrate.
      </p>
    </div>
    <div class="filter-chips">
      <button class="filter-chip is-active" data-filter="all" style="--chip-color: var(--teal)">All</button>
      ${filterChips}
    </div>
    ${groupedContent}
  `);
}

function bindFilters() {
  if (route !== "work") return;

  document.addEventListener("click", (event) => {
    const chip = event.target.closest("[data-filter]");
    if (!chip) return;

    const filter = chip.dataset.filter;
    document.querySelectorAll(".filter-chip").forEach((c) => c.classList.remove("is-active"));
    chip.classList.add("is-active");

    document.querySelectorAll("[data-section-group]").forEach((group) => {
      const show = filter === "all" || group.dataset.sectionGroup === filter;
      group.style.display = show ? "" : "none";
      if (show && filter !== "all") group.open = true;
    });
  });
}

function renderProject() {
  const project = getProject(routeId);
  if (!project) return renderNotFound("Project not found");
  const role = getRole(project.roleId);
  const section = role ? getSection(role.sectionId) : sections[0];

  return shell(`
    <article class="project-detail" style="--area-color: ${section.accent}">
      <div class="page-header">
        ${introKicker(`${section.title} / ${role?.title || ""}`)}
        <h1>${escapeHtml(project.title)}</h1>
        <div class="project-meta-row">
          ${statusPill(project.status)}
          <span>${escapeHtml(project.date)}</span>
        </div>
        <p>${escapeHtml(project.summary)}</p>
      </div>

      <div class="detail-grid">
        <section>
          <h2>Objective</h2>
          <p>${escapeHtml(project.objective)}</p>
        </section>
        <section>
          <h2>Context / Problem</h2>
          <p>${escapeHtml(project.context)}</p>
        </section>
        <section>
          <h2>Methodology / Approach</h2>
          <p>${escapeHtml(project.approach)}</p>
        </section>
        <section>
          <h2>Output / Result</h2>
          <p>${escapeHtml(project.result)}</p>
        </section>
      </div>

      <aside class="detail-aside">
        <div>
          <h2>Skills demonstrated</h2>
          ${tags(project.skills)}
        </div>
        <div>
          <h2>Tools used</h2>
          ${tags(project.tools)}
        </div>
        <div>
          <h2>Documents</h2>
          ${
            project.files.length
              ? `<div class="file-list">${project.files
                  .map((file) => {
                    const url = viewerUrl(file, project.id);
                    if (url) {
                      return `<a href="${escapeHtml(url)}"><span>${escapeHtml(file.label.replace(/\.\w+$/, ""))}</span><small>View PDF</small></a>`;
                    }
                    if (file.type === "Image") {
                      return `<a href="${escapeHtml(file.path)}" target="_blank"><span>${escapeHtml(file.label)}</span><small>View image</small></a>`;
                    }
                    return "";
                  })
                  .filter(Boolean)
                  .join("")}</div>`
              : `<p class="empty-state">Documents will be added when the project is complete.</p>`
          }
        </div>
      </aside>
    </article>
  `);
}

function renderContact() {
  return shell(`
    <div class="page-header">
      ${introKicker("Contact")}
      <h1>Get in touch.</h1>
      <p>Reach out via email, phone, or connect on LinkedIn.</p>
    </div>
    <div class="contact-list">
      <a href="mailto:gilalmeida-2005@hotmail.com"><span>Email</span><strong>gilalmeida-2005@hotmail.com</strong></a>
      <a href="tel:+447377254057"><span>Phone</span><strong>+44 7377 254057</strong></a>
      <a href="${escapeHtml(profile.linkedIn)}"><span>LinkedIn</span><strong>Virgilio MF Almeida</strong></a>
    </div>
  `);
}

function renderNotFound(message = "Page not found") {
  return shell(`
    <div class="page-header">
      ${introKicker("Missing")}
      <h1>${escapeHtml(message)}</h1>
      <p>The matching data record was not found.</p>
      <a class="button primary" href="/">Return home</a>
    </div>
  `);
}

function renderRoute() {
  const routes = {
    home: renderHome,
    about: renderAbout,
    work: renderWork,
    "work-detail": renderProject,
    contact: renderContact,
  };

  app.innerHTML = (routes[route] || renderNotFound)();
}

renderSidebar();
renderRoute();
renderBreadcrumb();
bindNavigation();
bindFilters();


document.querySelectorAll("[data-current-year]").forEach((element) => {
  element.textContent = String(new Date().getFullYear());
});

document.querySelectorAll(".footer > span").forEach((el) => {
  if (!el.querySelector(".footer-cross")) {
    el.insertAdjacentHTML("afterbegin", `<span class="footer-cross">${crossSvg(12)}</span>`);
  }
});
