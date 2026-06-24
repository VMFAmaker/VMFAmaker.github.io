export type PortfolioStatus = "Completed" | "In Progress" | "Experimental" | "Conceptual";

export type SupportingFile = {
  label: string;
  type: "PDF" | "Image" | "Document" | "Dataset" | "Note";
  href: string;
  embedReady: boolean;
};

export type PortfolioProject = {
  id: string;
  title: string;
  date: string;
  status: PortfolioStatus;
  summary: string;
  skills: string[];
  tools: string[];
  objective: string;
  context: string;
  methodology: string;
  output: string;
  supportingFiles: SupportingFile[];
};

export type PortfolioCategory = {
  id: string;
  title: string;
  folderName: string;
  icon: "strategy" | "research" | "operations" | "business" | "development" | "experiments" | "analytics" | "writing";
  accent: string;
  description: string;
  projects: PortfolioProject[];
};

export const statusAccent: Record<PortfolioStatus, string> = {
  Completed: "#6FAE8E",
  "In Progress": "#7AA7FF",
  Experimental: "#D9A441",
  Conceptual: "#54B6B2",
};

export const portfolioCategories: PortfolioCategory[] = [
  {
    id: "strategy",
    title: "Strategy",
    folderName: "Strategy",
    icon: "strategy",
    accent: "#54B6B2",
    description: "Market logic, decision systems, positioning, and structured choices under uncertainty.",
    projects: [
      {
        id: "strategy-market-entry",
        title: "Market Entry Decision Map",
        date: "Started 2026",
        status: "Conceptual",
        summary: "A repeatable strategy canvas for comparing geographies, channels, constraints, and execution risk.",
        skills: ["Strategic analysis", "Scenario framing", "Prioritisation"],
        tools: ["Decision matrix", "Research notes", "PDF brief"],
        objective: "Design a concise method for deciding where and how a new product, service, or venture should enter a market.",
        context: "Early strategic ideas often collapse into broad opportunity lists. This project turns them into a staged archive of assumptions, evidence, and decision criteria.",
        methodology: "The system separates attractiveness, access, operational feasibility, and timing. Each dimension is scored, annotated, and linked back to source material.",
        output: "A modular report template that can become a strategy brief, a board note, or a personal learning artefact.",
        supportingFiles: [
          {
            label: "Market entry report placeholder",
            type: "PDF",
            href: "/portfolio/strategy/market-entry-decision-map.pdf",
            embedReady: true,
          },
          {
            label: "Source evidence index",
            type: "Dataset",
            href: "/portfolio/strategy/source-evidence-index.csv",
            embedReady: false,
          },
        ],
      },
      {
        id: "strategy-confidential-cases",
        title: "Confidential Strategy Case Abstracts",
        date: "Ongoing",
        status: "In Progress",
        summary: "An NDA-aware pattern library for describing strategy work without exposing sensitive client context.",
        skills: ["Abstraction", "Confidentiality", "Executive synthesis"],
        tools: ["Case note template", "Metadata tags"],
        objective: "Create a way to preserve learning value from professional work while removing company, client, and commercial details.",
        context: "Some professional work cannot be displayed directly. The portfolio needs a method for showing skill, judgement, and process without breaching trust.",
        methodology: "Sensitive projects are converted into abstract case notes containing problem type, decision pressure, methods used, and transferable learning.",
        output: "A controlled case format that can sit beside public projects while clearly marking confidentiality boundaries.",
        supportingFiles: [
          {
            label: "Abstract case note template",
            type: "Document",
            href: "/portfolio/strategy/confidential-case-note-template.docx",
            embedReady: false,
          },
        ],
      },
    ],
  },
  {
    id: "research",
    title: "Research",
    folderName: "Research",
    icon: "research",
    accent: "#7AA7FF",
    description: "Inquiry systems, source maps, literature notes, interviews, and research artefacts.",
    projects: [
      {
        id: "research-ai-operations",
        title: "AI in Small Business Operations",
        date: "Started 2026",
        status: "In Progress",
        summary: "A research file on how small firms can use AI for administration, sales support, and decision workflows.",
        skills: ["Secondary research", "Source evaluation", "Synthesis"],
        tools: ["Research matrix", "Annotated bibliography", "Interview guide"],
        objective: "Understand where AI meaningfully reduces operational drag for small businesses without creating unnecessary complexity.",
        context: "AI adoption is often discussed at enterprise scale. This research keeps attention on small teams, owner-led operations, and practical constraints.",
        methodology: "Sources are categorised by use case, maturity, risk, and implementation burden. Each finding is linked to notes and potential experiments.",
        output: "A living research dossier that can support reports, experiments, or future business development work.",
        supportingFiles: [
          {
            label: "Annotated source map",
            type: "PDF",
            href: "/portfolio/research/ai-small-business-source-map.pdf",
            embedReady: true,
          },
          {
            label: "Interview guide",
            type: "Document",
            href: "/portfolio/research/interview-guide.docx",
            embedReady: false,
          },
        ],
      },
    ],
  },
  {
    id: "operations",
    title: "Operations",
    folderName: "Operations",
    icon: "operations",
    accent: "#6FAE8E",
    description: "Processes, operating rhythms, service design, and workflow systems.",
    projects: [
      {
        id: "operations-weekly-control-room",
        title: "Weekly Control Room",
        date: "Started 2026",
        status: "Experimental",
        summary: "A personal operating system for translating projects, classes, research, and commitments into weekly decisions.",
        skills: ["Workflow design", "Prioritisation", "Review systems"],
        tools: ["Kanban", "Weekly review", "Operating metrics"],
        objective: "Create a clear weekly rhythm for managing multidisciplinary work without losing strategic context.",
        context: "A student portfolio can become fragmented when academic, professional, and experimental work are tracked separately.",
        methodology: "Inputs are separated into commitments, research threads, build work, and reflection. Each week produces decisions, not just task lists.",
        output: "A repeatable operating cadence that can later feed this website with project updates and status changes.",
        supportingFiles: [
          {
            label: "Weekly review image placeholder",
            type: "Image",
            href: "/portfolio/operations/weekly-control-room.png",
            embedReady: true,
          },
        ],
      },
    ],
  },
  {
    id: "business",
    title: "Business",
    folderName: "Business",
    icon: "business",
    accent: "#D9A441",
    description: "Commercial reasoning, venture analysis, business models, and management artefacts.",
    projects: [
      {
        id: "business-model-archive",
        title: "Business Model Archive",
        date: "Started 2026",
        status: "Conceptual",
        summary: "A catalogue of business model patterns with notes on incentives, margin structure, and operational constraints.",
        skills: ["Business modelling", "Commercial analysis", "Pattern recognition"],
        tools: ["Business model canvas", "Unit economics notes"],
        objective: "Build a reusable reference system for comparing how organisations create, capture, and defend value.",
        context: "Business model analysis is more useful when each example is stored as a pattern that can be compared across industries.",
        methodology: "Each entry records customer, offer, channel, revenue logic, cost drivers, operating complexity, and strategic tension.",
        output: "A searchable archive that can later become a database-backed knowledge system.",
        supportingFiles: [
          {
            label: "Business model note template",
            type: "Note",
            href: "/portfolio/business/business-model-note-template.md",
            embedReady: false,
          },
        ],
      },
    ],
  },
  {
    id: "development",
    title: "Development",
    folderName: "Development",
    icon: "development",
    accent: "#7AA7FF",
    description: "Technology builds, prototypes, interface systems, and implementation notes.",
    projects: [
      {
        id: "development-portfolio-knowledge-system",
        title: "Portfolio Knowledge System",
        date: "Completed 2026",
        status: "Completed",
        summary: "The first version of this website, structured for category mapping, project detail views, and future file ingestion.",
        skills: ["Frontend architecture", "Information design", "Data modelling"],
        tools: ["Next.js", "TypeScript", "Tailwind CSS"],
        objective: "Turn a personal website into a scalable archive for projects, reports, experiments, and thinking systems.",
        context: "A conventional portfolio presents finished work. This system also preserves process, unfinished ideas, and research structure.",
        methodology: "The site is driven by typed content arrays, repeatable category templates, anchor-based detail views, and a folder-to-category model.",
        output: "A production-ready static portfolio interface with a clear route toward metadata ingestion and document indexing.",
        supportingFiles: [
          {
            label: "Portfolio metadata template",
            type: "Dataset",
            href: "/portfolio/portfolio-metadata.template.json",
            embedReady: false,
          },
        ],
      },
    ],
  },
  {
    id: "experiments",
    title: "Experiments",
    folderName: "Experiments",
    icon: "experiments",
    accent: "#54B6B2",
    description: "Prototypes, unfinished systems, mock reports, tests, and speculative work.",
    projects: [
      {
        id: "experiments-report-lab",
        title: "Mock Report Lab",
        date: "Ongoing",
        status: "Experimental",
        summary: "A controlled space for testing report structures, visual systems, and executive communication formats.",
        skills: ["Rapid prototyping", "Visual synthesis", "Structured writing"],
        tools: ["PDF mockups", "Slide outlines", "Critique notes"],
        objective: "Use mock reports to practise communicating complex ideas with restraint, evidence, and strategic clarity.",
        context: "Not every learning artefact is a finished project. Some are experiments in judgement, format, and framing.",
        methodology: "Each mock report has a hypothesis, target audience, evidence structure, visual system, and post-build critique.",
        output: "A library of report experiments that can be reviewed, refined, or promoted into formal projects.",
        supportingFiles: [
          {
            label: "Mock report placeholder",
            type: "PDF",
            href: "/portfolio/experiments/mock-report-lab.pdf",
            embedReady: true,
          },
        ],
      },
    ],
  },
  {
    id: "analytics",
    title: "Analytics",
    folderName: "Analytics",
    icon: "analytics",
    accent: "#6FAE8E",
    description: "Measurement systems, dashboards, analytical models, and decision evidence.",
    projects: [
      {
        id: "analytics-learning-dashboard",
        title: "Learning Dashboard Model",
        date: "Started 2026",
        status: "Conceptual",
        summary: "A lightweight model for tracking learning velocity, project maturity, and evidence gathered across domains.",
        skills: ["Metrics design", "Data structure", "Analytical reasoning"],
        tools: ["Spreadsheet model", "JSON metadata", "Charts"],
        objective: "Define useful indicators for a multidisciplinary learning system without reducing work to vanity metrics.",
        context: "Personal analytics can become noisy. This project focuses on indicators that improve decisions about attention and depth.",
        methodology: "Metrics are grouped into progress, evidence, reuse potential, confidence, and next action clarity.",
        output: "A dashboard specification that can later connect to the folder ingestion and document indexing system.",
        supportingFiles: [
          {
            label: "Dashboard specification",
            type: "Document",
            href: "/portfolio/analytics/learning-dashboard-spec.md",
            embedReady: false,
          },
        ],
      },
    ],
  },
  {
    id: "writing",
    title: "Writing / Philosophy",
    folderName: "Writing",
    icon: "writing",
    accent: "#D9A441",
    description: "Essays, conceptual notes, reflective systems, and philosophical fragments.",
    projects: [
      {
        id: "writing-systems-thinking-notes",
        title: "Systems Thinking Notes",
        date: "Ongoing",
        status: "In Progress",
        summary: "A collection of short essays and notes on systems, incentives, identity, and disciplined learning.",
        skills: ["Conceptual writing", "Critical reflection", "Synthesis"],
        tools: ["Markdown notes", "Essay drafts", "Reading logs"],
        objective: "Develop a written record of thinking patterns that connect strategy, research, operations, and technology.",
        context: "The portfolio is not only a showcase. It is also a record of how ideas are formed, tested, and revised.",
        methodology: "Notes are tagged by concept, source, question, and application. Strong fragments can become essays or project framing.",
        output: "A philosophical layer that gives the technical and analytical work a clearer intellectual spine.",
        supportingFiles: [
          {
            label: "Essay draft placeholder",
            type: "Note",
            href: "/portfolio/writing/systems-thinking-notes.md",
            embedReady: false,
          },
        ],
      },
    ],
  },
];

export const portfolioFolderMap = portfolioCategories.map((category) => ({
  categoryId: category.id,
  websiteSection: `#category-${category.id}`,
  localFolder: `Portfolio/${category.folderName}`,
  publicAssetPath: `/portfolio/${category.id}`,
}));

export const currentFocusAreas = [
  "AI-enabled operating systems for small organisations",
  "Strategic analysis and market logic",
  "Research systems that preserve evidence and uncertainty",
  "Portfolio architecture as a living knowledge base",
];

