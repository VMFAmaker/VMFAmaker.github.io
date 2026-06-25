export const profile = {
  name: "Virgilio MF Almeida",
  role: "O segredo é so bulir",
  subtitle:
    "Structured portfolio across Business Management, Finance, Marketing, and Academic Research — organised by role and supported by real deliverables.",
  academic: "BBA, SP Jain London",
  graduation: "2028",
  languages: [
    { name: "Portuguese", level: "Native" },
    { name: "Spanish", level: "C2" },
    { name: "English", level: "C2" },
    { name: "French", level: "B1" },
  ],
  qualifications: [
    { title: "BBA — Bachelor of Business Administration", institution: "SP Jain London", period: "2024–2028" },
    { title: "A-Levels", institution: "Blenheim Highschool", period: "2022–2024", grades: "Spanish B, Business B, Mathematics C, Physics C, Psychology D" },
  ],
  experience: [
    { role: "Youth Counsellor & Pastor Assistant", type: "Volunteer", period: "Feb 2022 – Present", company: "ICMAV London Ltd", location: "Epsom" },
    { role: "Marketing Intern", period: "Jan 2025 – May 2025", company: "Shiok Kitchen Catering", location: "Singapore" },
    { role: "Waiter", period: "Jan 2023 – Apr 2025", company: "El Rincon", location: "Tottenham Corner" },
    { role: "Teacher Assistant", type: "Volunteer", period: "May 2023 – Jul 2023", company: "Blenheim High School", location: "Epsom" },
    { role: "Private Tutor", period: "Oct 2023 – Dec 2024 & Aug 2025 – Present", company: "Freelance", location: "Remote" },
  ],
  email: "gilalmeida-2005@hotmail.com",
  linkedIn: "https://www.linkedin.com/in/virgilio-mf-almeida",
};

export const statusStyles = {
  Completed: {
    label: "Completed",
    color: "#6f9f82",
  },
  Active: {
    label: "Active",
    color: "#6f91c9",
  },
  Draft: {
    label: "Draft",
    color: "#c59a4a",
  },
  Planned: {
    label: "Planned",
    color: "#8a929d",
  },
};

/* ─── Sections (top-level portfolio areas) ─── */

export const sections = [
  {
    id: "business-management",
    title: "Business Management",
    accent: "#58b6ad",
    summary: "Diagnosis, planning, decision-making, and execution across advisory, strategy, and project delivery work.",
  },
  {
    id: "finance",
    title: "Finance",
    accent: "#7397d8",
    summary: "Recording, analysing, forecasting, valuing, and modelling — with professional tools and numerical discipline.",
  },
  {
    id: "marketing",
    title: "Marketing",
    accent: "#c59a4a",
    summary: "Audience understanding, visual communication, campaign planning, and market-facing strategy.",
  },
  {
    id: "academic-research",
    title: "Academic Research",
    accent: "#76a982",
    summary: "Scholarly development, critical thinking, evidence handling, and structured academic writing.",
  },
];

/* ─── Roles (sub-folders within each section) ─── */

export const roles = [
  // Business Management
  {
    id: "business-counselling",
    sectionId: "business-management",
    title: "Business Counselling",
    summary: "Advisory work that evaluates a business situation and recommends what management should do next.",
    tools: ["Word", "Excel", "PowerPoint"],
  },
  {
    id: "business-plans",
    sectionId: "business-management",
    title: "Business Plans",
    summary: "Design and test a new business or venture concept with financial projections and pitch decks.",
    tools: ["Word", "Excel", "PowerPoint", "Design tools"],
  },
  {
    id: "strategy-analysis",
    sectionId: "business-management",
    title: "Strategy & Business Analysis",
    summary: "Deeper investigative work on business performance, processes, markets, and strategic options.",
    tools: ["Word", "Excel", "PowerPoint", "Python"],
  },
  {
    id: "operations-pm",
    sectionId: "business-management",
    title: "Operations & Project Management",
    summary: "Sequencing, controlling, monitoring, and delivering activities with execution discipline.",
    tools: ["Excel", "Word", "PowerPoint", "Python"],
  },
  // Finance
  {
    id: "investment",
    sectionId: "finance",
    title: "Investment",
    summary: "Analysing securities, companies, industries, or portfolios to support investment decisions.",
    tools: ["Excel", "Word", "PowerPoint", "Python"],
  },
  {
    id: "accountant",
    sectionId: "finance",
    title: "Accountant",
    summary: "Recording, organising, checking, and presenting financial information accurately.",
    tools: ["Excel", "Word", "PowerPoint"],
  },
  {
    id: "financial-analyst",
    sectionId: "finance",
    title: "Financial Analyst",
    summary: "Understanding business performance and forecasting future outcomes through KPI analysis and dashboards.",
    tools: ["Excel", "Word", "PowerPoint", "Python"],
  },
  {
    id: "corporate-finance",
    sectionId: "finance",
    title: "Corporate Finance",
    summary: "Funding, capital structure, valuation, M&A evaluation, and financial decision-making inside a business.",
    tools: ["Excel", "Word", "PowerPoint", "Python"],
  },
  {
    id: "quant-analyst",
    sectionId: "finance",
    title: "Quantitative Analyst",
    summary: "Mathematically driven models for finance and risk — statistical modelling, simulation, and backtesting.",
    tools: ["Python", "Excel", "Word", "PowerPoint"],
  },
  // Marketing
  {
    id: "graphic-design",
    sectionId: "marketing",
    title: "Graphic Design",
    summary: "Visual brand and campaign assets — posters, social graphics, brand sheets, and infographics.",
    tools: ["Canva", "Adobe tools", "PowerPoint"],
  },
  {
    id: "marketing-plans",
    sectionId: "marketing",
    title: "Marketing Plans",
    summary: "Structured campaign planning, go-to-market strategy, and market-facing communication.",
    tools: ["Word", "Excel", "PowerPoint"],
  },
  // Academic Research
  {
    id: "research-papers",
    sectionId: "academic-research",
    title: "Research Papers",
    summary: "Completed or near-final academic work showing mature argument, evidence use, and scholarly rigour.",
    tools: ["Word"],
  },
  {
    id: "research-drafts",
    sectionId: "academic-research",
    title: "Research Drafts",
    summary: "Developmental material showing how research ideas evolved through drafting and revision.",
    tools: ["Word"],
  },
];

/* ─── Projects (manual entries — these override synced data for the same id) ─── */

const manualProjects = [
  {
    id: "az-retail-report",
    roleId: "business-counselling",
    title: "AZ Retail Group — Counselling Report",
    status: "Draft",
    date: "2026-02",
    summary:
      "Practice advisory report evaluating margin resilience, competitive positioning, and operational efficiency for a major retail group.",
    objective:
      "Diagnose key strategic issues and deliver prioritised, evidence-backed recommendations for profitability improvement over a 12–36 month horizon.",
    context:
      "Retail margins face pressure from tariffs, wages, logistics costs, and competitive pricing from omnichannel and cross-border platforms. International operations structurally underperform North America.",
    approach:
      "Public data modelling, SWOT analysis, Porter's Five Forces, margin decomposition, initiative prioritisation with economic impact estimates, and a 12-month action plan with KPIs.",
    result:
      "Draft advisory report identifying a $4.5–7B profit opportunity through international margin closure and convenience-led competitive strategy.",
    skills: ["Business judgement", "Evidence-based recommendation", "Executive writing", "Financial modelling", "Issue prioritisation"],
    tools: ["Word"],
    files: [
      { label: "A-Z Report.docx", type: "Word", path: "/files/business-counselling/a-z-report/A-Z Report.docx" },
    ],
  },
  {
    id: "nicholas-cars-report",
    roleId: "business-counselling",
    title: "Nicholas Cars — Counselling Report",
    status: "Draft",
    date: "2026-02",
    summary:
      "Practice advisory report on margin resilience, autonomy execution risk, and competitive positioning for an EV manufacturer.",
    objective:
      "Identify practical initiatives to restore automotive profitability and defend market leadership against Chinese EV commoditisation.",
    context:
      "Automotive margins collapsed from 18.2% to 8.2% amid China price wars. US battery costs run 2x China. Autonomy deployment lags Chinese OEMs by 18–24 months.",
    approach:
      "Public data modelling, competitive gap analysis, SWOT, segment performance review, two strategic mandates with economic forecasts and institutional friction analysis.",
    result:
      "Draft report recommending a frugal engineering pivot ($8.2B FY27 uplift) and autonomy regulatory unlock ($10B revenue opportunity).",
    skills: ["Strategic diagnosis", "Competitive analysis", "Financial modelling", "Management recommendation", "Report structuring"],
    tools: ["Word"],
    files: [
      { label: "Nicholas Cars Report.docx", type: "Word", path: "/files/business-counselling/nicholas-cars/Nicholas Cars Report.docx" },
    ],
  },
  {
    id: "dcf-valuation",
    roleId: "corporate-finance",
    title: "DCF Valuation & Capital Structure Analysis",
    status: "Planned",
    date: "2026-06",
    summary:
      "Full DCF valuation of a public company with WACC calculation, capital structure testing, and investment recommendation.",
    objective:
      "Build a complete valuation model and assess whether the company is over/undervalued, with recommendations on optimal funding structure.",
    context:
      "Core corporate finance exercise demonstrating valuation discipline, cost of capital reasoning, and capital structure trade-offs.",
    approach:
      "DCF model in Excel, WACC from comparable firms, sensitivity analysis on key assumptions, written valuation report, board-level summary deck.",
    result:
      "Excel valuation model, Word report, and PowerPoint summary — demonstrating end-to-end corporate finance judgement.",
    skills: ["DCF valuation", "WACC calculation", "Capital structure analysis", "Sensitivity analysis", "Financial communication"],
    tools: ["Excel", "Word", "PowerPoint"],
    files: [],
  },
  {
    id: "ma-deal-evaluation",
    roleId: "corporate-finance",
    title: "M&A Deal Evaluation",
    status: "Planned",
    date: "2026-07",
    summary:
      "Evaluation of a real or hypothetical acquisition — synergy modelling, premium assessment, and financing option comparison.",
    objective:
      "Assess whether an acquisition creates or destroys value, and recommend the optimal financing approach.",
    context:
      "M&A analysis covering deal rationale, synergy estimates, accretion/dilution, and financing trade-offs between cash, stock, and debt.",
    approach:
      "Merger model in Excel, synergy and premium analysis, accretion/dilution testing, deal evaluation memo, investment committee-style slides.",
    result:
      "Excel merger model, Word deal memo, and PowerPoint recommendation deck.",
    skills: ["M&A analysis", "Synergy modelling", "Accretion/dilution", "Deal structuring", "Financial presentation"],
    tools: ["Excel", "Word", "PowerPoint"],
    files: [],
  },
  {
    id: "working-capital-review",
    roleId: "corporate-finance",
    title: "Working Capital & Cash Management Review",
    status: "Planned",
    date: "2026-07",
    summary:
      "Analysis of a company's working capital efficiency with recommendations for cash flow improvement.",
    objective:
      "Identify where cash is trapped in receivables, payables, and inventory cycles, and recommend practical improvements.",
    context:
      "Operational side of corporate finance linking to business counselling — showing how liquidity management connects to strategic health.",
    approach:
      "Working capital model in Excel, cash conversion cycle analysis, scenario testing, management advisory report, CFO briefing deck.",
    result:
      "Excel working capital model, Word advisory report, and PowerPoint briefing.",
    skills: ["Liquidity management", "Cash conversion analysis", "Operational finance", "Scenario modelling", "Advisory writing"],
    tools: ["Excel", "Word", "PowerPoint"],
    files: [],
  },
];

/* ─── Synced projects (auto-generated by tools/sync.mjs) ─── */

let syncedProjects = [];
try {
  const module = await import("./projects-sync.mjs");
  syncedProjects = module.default || [];
} catch {
  // No synced projects yet — run `npm run sync` to generate
}

const skillsOverrides = {
  "nicholas-cars": ["Business analysis", "Strategic diagnosis", "Financial analysis", "Executive writing", "Data analysis", "Competitive analysis", "Report structuring"],
  "knowledgeable-new": ["Business planning", "Financial modelling", "Market analysis", "Strategic planning", "Pitch presentation", "Action planning", "Feasibility analysis"],
  "knowledgeable-old": ["Business planning", "Financial modelling", "Market research", "Strategic thinking", "Pitch development", "Action planning", "Risk assessment"],
  "layerstone": ["Business planning", "Financial modelling", "Market analysis", "Strategic planning", "Pitch presentation", "Action planning", "Competitive positioning"],
  "mustard-seed": ["Business planning", "Financial modelling", "Market research", "Strategic planning", "Pitch presentation", "Action planning", "Startup feasibility"],
  "meridian-digital-holding": ["Investment analysis", "Financial modelling", "Valuation", "Due diligence", "Pitch deck creation", "Report writing", "Market assessment"],
  "project-apex": ["Risk modelling", "Quantitative analysis", "Statistical analysis", "Monte Carlo simulation", "VaR calculation", "Data visualisation", "Portfolio risk assessment"],
  "rip-2-report-copy": ["Academic writing", "Critical analysis", "Evidence evaluation", "Research methodology", "Literature review", "Structured argumentation", "Citation management"],
};

const manualIds = new Set(manualProjects.map((p) => p.id));
const mergedSynced = syncedProjects
  .filter((p) => !manualIds.has(p.id))
  .map((p) => skillsOverrides[p.id] ? { ...p, skills: skillsOverrides[p.id] } : p);
export const projects = [...manualProjects, ...mergedSynced];

export const thinkingEntries = [
  {
    title: "A portfolio as an operating system",
    date: "2026-05",
    summary:
      "The useful portfolio is not a gallery. It is a structured memory system for evidence, decisions, and learning loops.",
  },
  {
    title: "Emerging operator, not influencer",
    date: "2026-05",
    summary:
      "The tone of this website should emphasise coordination, judgement, communication, leadership, and research discipline.",
  },
  {
    title: "Confidentiality as design constraint",
    date: "2026-05",
    summary:
      "Some work should be abstracted rather than displayed. A good archive can show capability while protecting trust.",
  },
];

/* ─── Scripture ─── */

export const scriptures = {
  "home-top": {
    verse: "The fear of the LORD is the beginning of knowledge, but fools despise wisdom and instruction.",
    reference: "Proverbs 1:7 — NIV",
  },
  "home-bottom": {
    verse: "But seek ye first the kingdom of God, and his righteousness; and all these things shall be added unto you.",
    reference: "Matthew 6:33 — KJV",
  },
  "business-management": {
    verse: "Commit to the LORD whatever you do, and he will establish your plans.",
    reference: "Proverbs 16:3 — NIV",
  },
  "finance": {
    verse: "Whoever loves money never has enough; whoever loves wealth is never satisfied with their income. This too is meaningless.",
    reference: "Ecclesiastes 5:10 — NIV",
  },
  "academic-research": {
    verse: "An intelligent heart acquires knowledge, and the ear of the wise seeks knowledge.",
    reference: "Proverbs 18:15 — ESV",
  },
};

/* ─── Helper functions ─── */

export function getSection(sectionId) {
  return sections.find((s) => s.id === sectionId);
}

export function getRole(roleId) {
  return roles.find((r) => r.id === roleId);
}

export function getRolesBySection(sectionId) {
  return roles.filter((r) => r.sectionId === sectionId);
}

export function getProject(projectId) {
  return projects.find((p) => p.id === projectId);
}

export function getProjectsByRole(roleId) {
  return projects.filter((p) => p.roleId === roleId);
}

export function getProjectsBySection(sectionId) {
  const sectionRoles = getRolesBySection(sectionId).map((r) => r.id);
  return projects.filter((p) => sectionRoles.includes(p.roleId));
}

export function getSectionForProject(project) {
  const role = getRole(project.roleId);
  return role ? getSection(role.sectionId) : sections[0];
}
