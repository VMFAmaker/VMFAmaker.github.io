# VMFA Portfolio Website

Standalone static portfolio archive for Virgilio MF Almeida.

## Run Locally

```powershell
npm.cmd run generate
npm.cmd run dev
```

The local server defaults to:

```text
http://localhost:9004
```

To use another port:

```powershell
$env:PORT=9010; npm.cmd run dev
```

## Architecture

- `assets/js/content.mjs` is the main website data model.
- `assets/js/app.mjs` renders each page from route metadata.
- `assets/css/styles.css` contains the design system.
- `tools/generate-pages.mjs` generates dedicated static pages for areas and projects.
- `metadata.schema.json` describes the future project metadata contract.

## Navigation Structure

- Home
- About
- Areas of Work
- Projects
- Archive
- Thinking
- Contact

Area pages and project pages are generated from the data model.

