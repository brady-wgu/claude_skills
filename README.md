<h1 align="center">
  <br>
  Claude Skills Library
  <br>
</h1>

<p align="center">
  <strong>A collection of reusable skills for Claude Chat and Claude Code</strong><br>
  Built by Brady Redfearn &bull; Program Development, Western Governors University
</p>

<p align="center">
  <a href="#-about">About</a> &bull;
  <a href="#-skill-catalog">Skill Catalog</a> &bull;
  <a href="#-repo-structure">Repo Structure</a> &bull;
  <a href="#-how-to-use-a-skill">How to Use</a> &bull;
  <a href="#-adapting-skills-for-your-own-work">Adapting Skills</a>
</p>

---

## About

Everything in this repo is a **skill** -- a structured prompt or automation that extends what Claude can do. Skills range from simple text-processing templates to full end-to-end pipelines with API integrations.

This repo is organized into two categories based on where the skill runs:

| Category | Where It Runs | What It Can Do |
|----------|--------------|----------------|
| **Claude Code Skills** | Claude Code (CLI, Desktop, IDE) | Execute code, call APIs, read/write files, run shell commands |
| **Claude Chat Skills** | Claude Chat (web or app) | Text processing, analysis, formatting -- no tool access |

> **Note:** This repo serves as a backup and sharing directory. Skills are not executed from this repo directly. They are copied into the appropriate Claude environment (e.g., `~/.claude/plugins/` for Claude Code, or pasted into a Claude Chat project) before use.

---

## Skill Catalog

### Claude Code Skills

| Skill | Description | Status |
|-------|-------------|--------|
| [**blog-beast-pipeline**](claude-code-skills/blog-beast-pipeline/) | Automated daily workflow: processes raw work notes into a 7-section journal (BLOG), writes to Coda, pulls the task list from Coda, produces a 4-section morning briefing (BEAST) with task updates, and syncs everything back to Coda. Includes Python scripts for bidirectional Coda API integration. | Production |
| [**mmorpg-glossary**](claude-code-skills/mmorpg-glossary/) | WGU glossary CRUD tool. Python scripts provide reliable search, add, edit, and delete operations against the Glossary table in Coda. Includes an experimental Claude Code plugin for conversational access (plugin triggering is unreliable; scripts work directly). Web interface planned. | Beta |

### Claude Chat Skills

| Skill | Description | Status |
|-------|-------------|--------|
| [**blog-beast-pipeline**](claude-chat-skills/blog-beast-pipeline/) | Daily journal and task reconciliation. Coupled BLOG + BEAST: synthesizes raw OneNote notes into a Daily Log entry, then reconciles the BEAST task table against it. Writes directly to Coda via the Coda MCP (no CSV paste step). | Production |
| [**blog-beast-weekly-review**](claude-chat-skills/blog-beast-weekly-review/) | Weekly retrospective and integrity audit. Rolls up the prior Mon-Fri Daily Log entries into a Weekly BLOG entry, then runs a seven-check BEAST audit to catch discrepancies that daily cadence misses. | Production |
| [**blog-beast-monthly-review**](claude-chat-skills/blog-beast-monthly-review/) | Monthly retrospective and integrity audit. Rolls up the prior calendar month's Daily Log entries (cross-referenced against overlapping Weekly BLOGs) into a Monthly BLOG entry, then runs a ten-check BEAST audit. | Production |
| [**brady-document-style**](claude-chat-skills/brady-document-style/) | WGU document formatting standard. Applies consistent styling, structure, and tone to any document Claude creates or edits -- reports, briefs, market scans, user profiles, and more. | Stable |

---

## Repo Structure

```
claude_skills/
│
├── claude-code-skills/
│   ├── blog-beast-pipeline/                Full daily automation pipeline
│   │   ├── README.md                       Quick start and links
│   │   ├── CLAUDE.md                       Pointer to SKILL.md (source of truth)
│   │   ├── config.example.env              Template for .env configuration
│   │   ├── requirements.txt                Python dependencies
│   │   ├── docs/
│   │   │   └── SETUP.md                    Detailed setup guide
│   │   ├── scripts/
│   │   │   ├── discover_config.py          Auto-discover Coda table/column IDs
│   │   │   ├── pipeline_config.py          Shared config loader
│   │   │   ├── coda_client.py              Coda API wrapper
│   │   │   ├── blog_to_coda.py             Write BLOG entry to Coda
│   │   │   ├── beast_from_coda.py          Pull BEAST table from Coda
│   │   │   └── beast_to_coda.py            Upsert BEAST updates to Coda
│   │   └── plugin/
│   │       ├── .claude-plugin/
│   │       │   └── plugin.json             Plugin manifest
│   │       └── skills/
│   │           └── run-pipeline/
│   │               └── SKILL.md            Unified pipeline skill (source of truth)
│   │
│   └── mmorpg-glossary/                    WGU glossary CRUD tool
│       ├── CLAUDE.md                       Project instructions
│       ├── config.example.env              Template for Coda API key
│       ├── requirements.txt                Python dependencies
│       ├── docs/
│       │   └── SETUP.md                    Setup guide for colleagues
│       ├── scripts/
│       │   ├── coda_client.py              Coda API wrapper
│       │   ├── glossary_service.py         Glossary business logic
│       │   └── cli.py                      CLI bridge (called by skill)
│       └── plugin/
│           ├── .claude-plugin/
│           │   └── plugin.json             Plugin manifest
│           └── skills/
│               └── glossary/
│                   └── SKILL.md            Conversational glossary skill (/glossary)
│
└── claude-chat-skills/
    ├── blog-beast-pipeline/                Daily BLOG + BEAST pipeline (MCP-native)
    │   ├── SKILL.md                        Skill entry point and operating rules
    │   └── references/                     BLOG, BEAST, Coda schema, and safety guides
    ├── blog-beast-pipeline.zip             Packaged bundle for upload
    ├── blog-beast-weekly-review/           Weekly retrospective + 7-check BEAST audit
    │   ├── SKILL.md
    │   └── references/
    ├── blog-beast-weekly-review.zip
    ├── blog-beast-monthly-review/          Monthly retrospective + 10-check BEAST audit
    │   ├── SKILL.md
    │   └── references/
    ├── blog-beast-monthly-review.zip
    └── brady-document-style/               Document formatting standard
        └── brady-document-style.skill
```

---

## How to Use a Skill

### Claude Chat Skills

Chat skills ship as `.zip` bundles (newer BLOG/BEAST skills) or single `.skill` files (older-format skills like `brady-document-style`). Both are ZIP archives -- the only difference is the `.skill` extension.

1. Download the `.zip` or `.skill` file from the skill's folder
2. Open [Claude Chat](https://claude.ai) and navigate to **Settings -> Capabilities -> Skills**
3. Upload the file -- Claude Chat will unpack it and register the skill
4. Start a conversation; Claude will invoke the skill when the trigger phrases in its description match

> **Tip:** Each skill folder in this repo also contains an unpacked `SKILL.md` (plus a `references/` folder for the BLOG/BEAST skills). Read those directly if you want to review or customize the instructions before zipping and uploading.

### Claude Code Skills

Claude Code skills are more involved because they may include scripts, API integrations, and plugin manifests. Each skill folder contains its own setup instructions. General pattern:

1. Clone this repo
2. Follow the `SETUP.md` or `CLAUDE.md` in the skill's folder
3. Install the plugin by copying the `plugin/` directory to `~/.claude/plugins/`
4. Open Claude Code and use the trigger phrase (e.g., "run pipeline")

---

## Adapting Skills for Your Own Work

These skills were built for a specific workflow at WGU, but the patterns are portable. Here is how to make them your own:

### Claude Chat Skills

1. **Unzip the `.skill` file** to access the `SKILL.md` inside
2. **Edit the markdown** to match your role, terminology, and output format
3. **Re-zip** the folder (the folder name must match the skill name) and upload to your Claude project
4. Key things to customize:
   - Section headers and output structure
   - Field values and terminology (e.g., status names, project names)
   - Tone and formatting preferences
   - Any role-specific context (your title, team, acronyms)

### Claude Code Skills

1. **Fork this repo** or copy the skill folder you want
2. **Run `python scripts/discover_config.py`** to auto-configure your Coda table and column IDs (writes `config.json`)
3. **Update `coda_client.py`** -- set `ALLOWED_DOC_ID` to your Coda doc ID
4. **Edit the `SKILL.md`** pipeline spec to match your workflow: trigger phrases, processing logic, author context, and acronyms
5. **Replace the Python scripts** with your own API integrations if targeting a different tool (Notion, Airtable, etc.)

### General Principles

- **Skills are just structured prompts.** There is no magic -- every skill is a markdown file that tells Claude what to do, in what order, and in what format.
- **Start by copying, then customize.** It is easier to edit an existing skill than to write one from scratch.
- **Test in draft mode first.** Use `--dry-run` flags (where available) or set pipeline mode to `TEST` before going to production.
- **Keep sensitive data out of skills.** API keys go in `.env` files, never in skill definitions or prompts.

---

<p align="center">
  <sub>Built with Claude Code &bull; Questions? Reach out to Brady Redfearn in Program Development</sub>
</p>
