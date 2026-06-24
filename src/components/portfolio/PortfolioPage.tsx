import type { CSSProperties } from "react";
import {
  Archive,
  ArrowUpRight,
  BarChart3,
  BriefcaseBusiness,
  Building2,
  Code2,
  Database,
  FileText,
  FlaskConical,
  Folder,
  GraduationCap,
  Image,
  Languages,
  Layers3,
  Linkedin,
  LockKeyhole,
  Mail,
  Network,
  PenTool,
  Search,
  Settings2,
  ShieldCheck,
  Workflow,
} from "lucide-react";
import {
  currentFocusAreas,
  portfolioCategories,
  portfolioFolderMap,
  statusAccent,
  type PortfolioCategory,
  type PortfolioProject,
  type SupportingFile,
} from "@/lib/portfolio-data";

const iconMap = {
  strategy: BriefcaseBusiness,
  research: Search,
  operations: Settings2,
  business: Building2,
  development: Code2,
  experiments: FlaskConical,
  analytics: BarChart3,
  writing: PenTool,
};

function getCategoryStyle(category: PortfolioCategory): CSSProperties {
  return { "--category-accent": category.accent } as CSSProperties;
}

function CategoryCard({ category }: { category: PortfolioCategory }) {
  const Icon = iconMap[category.icon];

  return (
    <a
      href={`#category-${category.id}`}
      className="portfolio-card group flex min-h-[172px] flex-col justify-between border border-white/10 bg-[#101821]/78 p-5 outline-none transition duration-300 focus-visible:ring-2 focus-visible:ring-[var(--category-accent)]"
      style={getCategoryStyle(category)}
    >
      <div className="flex items-start justify-between gap-4">
        <Icon className="h-5 w-5 text-[var(--category-accent)]" strokeWidth={1.6} />
        <ArrowUpRight className="h-4 w-4 text-white/25 transition group-hover:text-[var(--category-accent)]" />
      </div>
      <div className="space-y-3">
        <h3 className="text-xl font-semibold tracking-[-0.01em] text-[#F4F5F6]">{category.title}</h3>
        <p className="max-w-[28rem] text-sm leading-6 text-[#AEB7C2]">{category.description}</p>
      </div>
    </a>
  );
}

function StatusTag({ status }: { status: PortfolioProject["status"] }) {
  return (
    <span
      className="inline-flex w-fit items-center border px-2.5 py-1 text-[0.68rem] font-semibold uppercase tracking-[0.16em]"
      style={{
        borderColor: `${statusAccent[status]}66`,
        color: statusAccent[status],
        background: `${statusAccent[status]}10`,
      }}
    >
      {status}
    </span>
  );
}

function ProjectCard({ category, project }: { category: PortfolioCategory; project: PortfolioProject }) {
  return (
    <a
      href={`#project-${project.id}`}
      className="portfolio-card group flex h-full min-h-[268px] flex-col justify-between border border-white/10 bg-[#0F151D]/92 p-5 outline-none transition duration-300 focus-visible:ring-2 focus-visible:ring-[var(--category-accent)]"
      style={getCategoryStyle(category)}
    >
      <div className="space-y-5">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <p className="text-xs uppercase tracking-[0.18em] text-[#7F8A96]">{project.date}</p>
          <StatusTag status={project.status} />
        </div>
        <div className="space-y-3">
          <h4 className="text-lg font-semibold leading-7 text-[#F2F4F5]">{project.title}</h4>
          <p className="text-sm leading-6 text-[#AEB7C2]">{project.summary}</p>
        </div>
      </div>
      <div className="space-y-4 pt-5">
        <div className="flex flex-wrap gap-2">
          {project.skills.slice(0, 3).map((skill) => (
            <span key={skill} className="border border-white/10 px-2.5 py-1 text-xs text-[#C5CCD3]">
              {skill}
            </span>
          ))}
        </div>
        <span className="inline-flex items-center gap-2 text-sm font-medium text-[var(--category-accent)]">
          Open detail
          <ArrowUpRight className="h-3.5 w-3.5" />
        </span>
      </div>
    </a>
  );
}

function SupportingFiles({ files }: { files: SupportingFile[] }) {
  const fileIcon = (type: SupportingFile["type"]) => {
    if (type === "Image") return Image;
    if (type === "Dataset") return Database;
    return FileText;
  };

  return (
    <div className="grid gap-3 sm:grid-cols-2">
      {files.map((file) => {
        const Icon = fileIcon(file.type);

        return (
          <a
            href={file.href}
            key={file.label}
            className="group flex min-h-[92px] items-start gap-3 border border-white/10 bg-[#0B0F14] p-4 transition hover:border-white/25"
          >
            <Icon className="mt-0.5 h-4 w-4 text-[#7AA7FF]" strokeWidth={1.7} />
            <span className="space-y-1">
              <span className="block text-sm font-medium text-[#E6E6E6]">{file.label}</span>
              <span className="block text-xs uppercase tracking-[0.16em] text-[#7F8A96]">
                {file.type} {file.embedReady ? "/ embed ready" : "/ indexed link"}
              </span>
            </span>
          </a>
        );
      })}
    </div>
  );
}

function ProjectDetail({ category, project }: { category: PortfolioCategory; project: PortfolioProject }) {
  const detailItems = [
    ["Objective", project.objective],
    ["Context / Problem", project.context],
    ["Methodology / Approach", project.methodology],
    ["Output / Result", project.output],
  ];

  return (
    <article
      id={`project-${project.id}`}
      className="scroll-mt-28 border border-white/10 bg-[#101821]/72 p-5 sm:p-6 lg:p-7"
      style={getCategoryStyle(category)}
    >
      <div className="mb-8 flex flex-col gap-5 border-b border-white/10 pb-6 md:flex-row md:items-start md:justify-between">
        <div className="space-y-3">
          <p className="text-xs uppercase tracking-[0.2em] text-[var(--category-accent)]">{category.title}</p>
          <h4 className="max-w-3xl text-2xl font-semibold tracking-[-0.02em] text-[#F3F5F6]">{project.title}</h4>
          <p className="text-sm text-[#97A2AE]">{project.date}</p>
        </div>
        <StatusTag status={project.status} />
      </div>

      <div className="grid gap-6 lg:grid-cols-[1.4fr_0.8fr]">
        <div className="grid gap-5">
          {detailItems.map(([label, value]) => (
            <section key={label} className="space-y-2">
              <h5 className="text-xs font-semibold uppercase tracking-[0.18em] text-[#7F8A96]">{label}</h5>
              <p className="text-sm leading-7 text-[#CED5DC]">{value}</p>
            </section>
          ))}
        </div>

        <aside className="space-y-6 border-t border-white/10 pt-6 lg:border-l lg:border-t-0 lg:pl-6 lg:pt-0">
          <section className="space-y-3">
            <h5 className="text-xs font-semibold uppercase tracking-[0.18em] text-[#7F8A96]">Skills Demonstrated</h5>
            <div className="flex flex-wrap gap-2">
              {project.skills.map((skill) => (
                <span key={skill} className="border border-white/10 px-2.5 py-1 text-xs text-[#D8DEE4]">
                  {skill}
                </span>
              ))}
            </div>
          </section>

          <section className="space-y-3">
            <h5 className="text-xs font-semibold uppercase tracking-[0.18em] text-[#7F8A96]">Tools</h5>
            <div className="flex flex-wrap gap-2">
              {project.tools.map((tool) => (
                <span key={tool} className="border border-white/10 px-2.5 py-1 text-xs text-[#B8C0C8]">
                  {tool}
                </span>
              ))}
            </div>
          </section>

          <section className="space-y-3">
            <h5 className="text-xs font-semibold uppercase tracking-[0.18em] text-[#7F8A96]">Supporting Files</h5>
            <SupportingFiles files={project.supportingFiles} />
          </section>
        </aside>
      </div>
    </article>
  );
}

function CategorySection({ category }: { category: PortfolioCategory }) {
  const Icon = iconMap[category.icon];

  return (
    <section id={`category-${category.id}`} className="scroll-mt-24 space-y-8" style={getCategoryStyle(category)}>
      <div className="flex flex-col gap-5 border-t border-white/10 pt-10 md:flex-row md:items-end md:justify-between">
        <div className="max-w-3xl space-y-4">
          <div className="inline-flex items-center gap-3 text-[var(--category-accent)]">
            <Icon className="h-5 w-5" strokeWidth={1.7} />
            <span className="text-xs font-semibold uppercase tracking-[0.22em]">Category</span>
          </div>
          <h3 className="text-4xl font-semibold tracking-[-0.04em] text-[#F4F5F6] md:text-5xl">{category.title}</h3>
          <p className="text-base leading-8 text-[#AEB7C2]">{category.description}</p>
        </div>
        <p className="w-fit border border-white/10 px-3 py-2 text-xs uppercase tracking-[0.18em] text-[#7F8A96]">
          Portfolio/{category.folderName}
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {category.projects.map((project) => (
          <ProjectCard key={project.id} category={category} project={project} />
        ))}
      </div>

      <div className="space-y-4">
        {category.projects.map((project) => (
          <ProjectDetail key={project.id} category={category} project={project} />
        ))}
      </div>
    </section>
  );
}

function HeroVisual() {
  return (
    <div className="relative min-h-[360px] overflow-hidden border border-white/10 bg-[#101821] p-6">
      <div className="absolute inset-0 portfolio-grid opacity-70" />
      <div className="relative flex h-full min-h-[310px] flex-col justify-between">
        <div className="flex justify-between gap-4">
          <div className="space-y-2">
            <p className="text-xs uppercase tracking-[0.2em] text-[#7F8A96]">Archive Index</p>
            <p className="text-3xl font-semibold text-[#E6E6E6]">08</p>
            <p className="text-sm text-[#AEB7C2]">active domains</p>
          </div>
          <Network className="h-7 w-7 text-[#54B6B2]" strokeWidth={1.4} />
        </div>

        <div className="grid grid-cols-4 gap-2">
          {portfolioCategories.map((category, index) => (
            <a
              href={`#category-${category.id}`}
              key={category.id}
              className="group min-h-20 border border-white/10 bg-[#0B0F14]/72 p-3 transition hover:border-[var(--category-accent)]"
              style={getCategoryStyle(category)}
              aria-label={category.title}
            >
              <span className="block text-[0.68rem] uppercase tracking-[0.14em] text-[#7F8A96]">0{index + 1}</span>
              <span className="mt-5 block h-1 w-full bg-[var(--category-accent)] opacity-70 transition group-hover:opacity-100" />
            </a>
          ))}
        </div>

        <div className="grid gap-3 sm:grid-cols-3">
          {["Identity", "Evidence", "Systems"].map((item) => (
            <div key={item} className="border border-white/10 bg-[#0B0F14]/78 p-3">
              <p className="text-xs uppercase tracking-[0.16em] text-[#7F8A96]">{item}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export function PortfolioPage() {
  return (
    <div className="min-h-screen bg-[#0B0F14] text-[#E6E6E6]">
      <header className="sticky top-0 z-40 border-b border-white/10 bg-[#0B0F14]/88 backdrop-blur-xl">
        <nav className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4 sm:px-8">
          <a href="#top" className="text-sm font-semibold tracking-[0.16em] text-[#E6E6E6]">
            VMFA
          </a>
          <div className="hidden items-center gap-5 text-xs uppercase tracking-[0.14em] text-[#9AA5B1] md:flex">
            <a href="#categories" className="transition hover:text-[#54B6B2]">
              Categories
            </a>
            <a href="#folder-system" className="transition hover:text-[#D9A441]">
              System
            </a>
            <a href="#about" className="transition hover:text-[#7AA7FF]">
              About
            </a>
          </div>
        </nav>
      </header>

      <main id="top">
        <section className="mx-auto grid max-w-7xl gap-12 px-5 py-16 sm:px-8 md:py-24 lg:grid-cols-[1.05fr_0.95fr] lg:items-center">
          <div className="space-y-10">
            <div className="space-y-6">
              <p className="text-xs font-semibold uppercase tracking-[0.28em] text-[#54B6B2]">Digital Research Archive</p>
              <div className="space-y-5">
                <h1 className="max-w-4xl text-5xl font-semibold tracking-[-0.06em] text-[#F6F7F8] sm:text-6xl lg:text-7xl">
                  Virgilio MF Almeida
                </h1>
                <p className="max-w-3xl text-xl leading-8 text-[#C9D0D8]">
                  Multidisciplinary systems thinker working across strategy, research, operations, and technology
                </p>
              </div>
            </div>

            <div className="grid gap-3 sm:grid-cols-3">
              <div className="border border-white/10 bg-[#101821]/70 p-4">
                <GraduationCap className="mb-4 h-5 w-5 text-[#D9A441]" strokeWidth={1.6} />
                <p className="text-sm font-medium text-[#E6E6E6]">BBA, SP Jain London</p>
                <p className="mt-1 text-sm text-[#8E99A6]">Graduation: 2028</p>
              </div>
              <div className="border border-white/10 bg-[#101821]/70 p-4 sm:col-span-2">
                <Languages className="mb-4 h-5 w-5 text-[#7AA7FF]" strokeWidth={1.6} />
                <p className="text-sm font-medium text-[#E6E6E6]">Portuguese | English | Spanish | French</p>
                <p className="mt-1 text-sm text-[#8E99A6]">Limited proficiency in French</p>
              </div>
            </div>
          </div>

          <HeroVisual />
        </section>

        <section className="border-y border-white/10 bg-[#0F151D]/72">
          <div className="mx-auto grid max-w-7xl gap-8 px-5 py-12 sm:px-8 lg:grid-cols-[0.85fr_1.15fr] lg:items-start">
            <div className="flex items-center gap-3 text-[#54B6B2]">
              <Layers3 className="h-5 w-5" strokeWidth={1.7} />
              <p className="text-xs font-semibold uppercase tracking-[0.22em]">Operating Philosophy</p>
            </div>
            <p className="max-w-4xl text-xl font-light leading-10 text-[#D6DCE2]">
              I approach work as a system of relationships: incentives, evidence, constraints, and execution rhythms.
              Structured analysis gives the work a spine; experimental learning keeps it alive. The goal is not to
              collect projects, but to build reusable ways of seeing, testing, and improving complex situations.
            </p>
          </div>
        </section>

        <section className="mx-auto grid max-w-7xl gap-5 px-5 py-12 sm:px-8 md:grid-cols-[0.75fr_1.25fr]">
          <div className="border border-white/10 bg-[#101821]/70 p-5">
            <LockKeyhole className="mb-5 h-5 w-5 text-[#D9A441]" strokeWidth={1.7} />
            <h2 className="text-lg font-semibold text-[#F1F3F4]">System Disclaimer</h2>
          </div>
          <div className="border border-white/10 bg-[#101821]/70 p-5">
            <p className="leading-8 text-[#B9C2CC]">
              This portfolio contains finished projects, experimental work, mock reports, research artefacts, and
              incomplete systems. Some professional work is excluded or abstracted due to confidentiality, with
              NDA-aware descriptions used where the learning value can be shared safely.
            </p>
          </div>
        </section>

        <section id="categories" className="mx-auto max-w-7xl space-y-8 px-5 py-12 sm:px-8">
          <div className="max-w-3xl space-y-4">
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-[#7AA7FF]">Core Navigation System</p>
            <h2 className="text-4xl font-semibold tracking-[-0.04em] text-[#F6F7F8] md:text-5xl">Explore by domain</h2>
            <p className="text-base leading-8 text-[#AEB7C2]">
              Each category mirrors a local folder and uses the same repeatable project structure: evidence, method,
              output, skills, and supporting files.
            </p>
          </div>
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            {portfolioCategories.map((category) => (
              <CategoryCard key={category.id} category={category} />
            ))}
          </div>
        </section>

        <section className="mx-auto max-w-7xl space-y-16 px-5 py-12 sm:px-8">
          {portfolioCategories.map((category) => (
            <CategorySection key={category.id} category={category} />
          ))}
        </section>

        <section id="folder-system" className="border-y border-white/10 bg-[#0F151D]/72">
          <div className="mx-auto grid max-w-7xl gap-8 px-5 py-14 sm:px-8 lg:grid-cols-[0.8fr_1.2fr]">
            <div className="space-y-5">
              <div className="flex items-center gap-3 text-[#54B6B2]">
                <Archive className="h-5 w-5" strokeWidth={1.7} />
                <p className="text-xs font-semibold uppercase tracking-[0.22em]">Portfolio Folder Integration</p>
              </div>
              <h2 className="text-3xl font-semibold tracking-[-0.03em] text-[#F6F7F8] md:text-4xl">
                Built for future ingestion
              </h2>
              <p className="leading-8 text-[#AEB7C2]">
                The local <code className="text-[#D8DEE4]">Portfolio</code> folder is designed as the content source of
                record. When automation is added, new files can be read, classified, indexed, and mapped into the
                correct website category.
              </p>
            </div>

            <div className="grid gap-3">
              {portfolioFolderMap.map((item) => (
                <div key={item.categoryId} className="grid gap-3 border border-white/10 bg-[#0B0F14] p-4 md:grid-cols-[1fr_1fr_1fr]">
                  <span className="flex items-center gap-2 text-sm font-medium text-[#E6E6E6]">
                    <Folder className="h-4 w-4 text-[#D9A441]" strokeWidth={1.6} />
                    {item.localFolder}
                  </span>
                  <span className="text-sm text-[#97A2AE]">{item.websiteSection}</span>
                  <span className="text-sm text-[#97A2AE]">{item.publicAssetPath}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="mx-auto grid max-w-7xl gap-4 px-5 pb-14 sm:px-8 md:grid-cols-3">
            <div className="border border-white/10 bg-[#101821]/70 p-5">
              <Database className="mb-4 h-5 w-5 text-[#7AA7FF]" strokeWidth={1.7} />
              <h3 className="mb-2 font-semibold text-[#F1F3F4]">JSON Metadata Mapping</h3>
              <p className="text-sm leading-7 text-[#AEB7C2]">
                <code className="text-[#D8DEE4]">Portfolio/portfolio-metadata.template.json</code> defines title,
                category, status, tags, files, and visibility.
              </p>
            </div>
            <div className="border border-white/10 bg-[#101821]/70 p-5">
              <Workflow className="mb-4 h-5 w-5 text-[#54B6B2]" strokeWidth={1.7} />
              <h3 className="mb-2 font-semibold text-[#F1F3F4]">File Ingestion Logic</h3>
              <p className="text-sm leading-7 text-[#AEB7C2]">
                A future watcher can detect new documents, infer category from folder path, and create draft metadata.
              </p>
            </div>
            <div className="border border-white/10 bg-[#101821]/70 p-5">
              <ShieldCheck className="mb-4 h-5 w-5 text-[#D9A441]" strokeWidth={1.7} />
              <h3 className="mb-2 font-semibold text-[#F1F3F4]">Document Indexing</h3>
              <p className="text-sm leading-7 text-[#AEB7C2]">
                Public, private, abstracted, and NDA-aware assets can be separated before anything is displayed.
              </p>
            </div>
          </div>
        </section>

        <section id="about" className="mx-auto grid max-w-7xl gap-8 px-5 py-16 sm:px-8 lg:grid-cols-[0.85fr_1.15fr]">
          <div className="space-y-5">
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-[#D9A441]">About</p>
            <h2 className="text-4xl font-semibold tracking-[-0.04em] text-[#F6F7F8]">Academic and intellectual profile</h2>
          </div>
          <div className="grid gap-5">
            <div className="border border-white/10 bg-[#101821]/70 p-5">
              <p className="leading-8 text-[#C8D0D8]">
                Virgilio MF Almeida is a BBA student at SP Jain London, graduating in 2028. His work sits across
                strategy, research, operations, business development, analytics, writing, and technology prototypes.
              </p>
            </div>
            <div className="grid gap-4 md:grid-cols-2">
              <div className="border border-white/10 bg-[#101821]/70 p-5">
                <h3 className="mb-3 text-sm font-semibold uppercase tracking-[0.16em] text-[#7F8A96]">Thinking Approach</h3>
                <p className="text-sm leading-7 text-[#B9C2CC]">
                  Analytical, interdisciplinary, and systems-oriented. The emphasis is on structure, evidence,
                  experimentation, and transferability across domains.
                </p>
              </div>
              <div className="border border-white/10 bg-[#101821]/70 p-5">
                <h3 className="mb-3 text-sm font-semibold uppercase tracking-[0.16em] text-[#7F8A96]">Languages</h3>
                <p className="text-sm leading-7 text-[#B9C2CC]">
                  Portuguese, English, Spanish, and French with limited French proficiency.
                </p>
              </div>
            </div>
            <div className="border border-white/10 bg-[#101821]/70 p-5">
              <h3 className="mb-4 text-sm font-semibold uppercase tracking-[0.16em] text-[#7F8A96]">Current Focus Areas</h3>
              <div className="grid gap-2 md:grid-cols-2">
                {currentFocusAreas.map((area) => (
                  <p key={area} className="border border-white/10 px-3 py-3 text-sm text-[#C8D0D8]">
                    {area}
                  </p>
                ))}
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t border-white/10 bg-[#080B0F]">
        <div className="mx-auto flex max-w-7xl flex-col gap-5 px-5 py-8 text-sm text-[#8E99A6] sm:px-8 md:flex-row md:items-center md:justify-between">
          <p>&copy; {new Date().getFullYear()} Virgilio MF Almeida. Structured as a living archive.</p>
          <div className="flex flex-wrap gap-4">
            <a href="mailto:email@example.com" className="inline-flex items-center gap-2 transition hover:text-[#54B6B2]">
              <Mail className="h-4 w-4" /> Email placeholder
            </a>
            <a href="https://www.linkedin.com/in/virgilio-mf-almeida" className="inline-flex items-center gap-2 transition hover:text-[#7AA7FF]">
              <Linkedin className="h-4 w-4" /> LinkedIn
            </a>
            <a href="#" className="inline-flex items-center gap-2 transition hover:text-[#D9A441]">
              <Archive className="h-4 w-4" /> VA website
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
