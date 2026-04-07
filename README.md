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

### Claude Chat Skills

| Skill | Description | Status |
|-------|-------------|--------|
| [**beast-morning-briefing**](claude-chat-skills/beast-morning-briefing/) | Standalone BEAST task analysis. Paste a CSV export of your task list and get a structured morning briefing: flags, recommended updates, an import-ready CSV, and a prioritized daily task list. | Stable |
| [**blog-daily-processor**](claude-chat-skills/blog-daily-processor/) | Standalone BLOG note processor. Paste raw daily work notes and get a 7-section professional journal entry: reviewed notes, polished summary, executive bullets, wins, blockers, category, and a private sensitive items log. | Stable |
| [**brady-document-style**](claude-chat-skills/brady-document-style/) | WGU document formatting standard. Applies consistent styling, structure, and tone to any document Claude creates or edits -- reports, briefs, market scans, user profiles, and more. | Stable |

---

## Repo Structure

```
claude_skills/
│
├── claude-code-skills/
│   └── blog-beast-pipeline/                Full daily automation pipeline
│       ├── CLAUDE.md                       Pipeline orchestration + specs
│       ├── config.example.env              Template for Coda API key
│       ├── requirements.txt                Python dependencies
│       ├── docs/
│       │   └── SETUP.md                    Detailed setup guide
│       ├── scripts/
│       │   ├── coda_client.py              Coda API wrapper
│       │   ├── blog_to_coda.py             Write BLOG entry to Coda
│       │   ├── beast_from_coda.py          Pull BEAST table from Coda
│       │   └── beast_to_coda.py            Upsert BEAST updates to Coda
│       └── plugin/
│           ├── .claude-plugin/
│           │   └── plugin.json             Plugin manifest
│           └── skills/
│               └── run-pipeline/
│                   └── SKILL.md            Unified pipeline skill
│
└── claude-chat-skills/
    ├── beast-morning-briefing/             Standalone BEAST analysis
    │   └── beast-morning-briefing.skill
    ├── blog-daily-processor/               Standalone BLOG processor
    │   └── blog-daily-processor.skill
    └── brady-document-style/               Document formatting standard
        └── brady-document-style.skill
```

---

## How to Use a Skill

### Claude Chat Skills (`.skill` files)

1. Download the `.skill` file from the appropriate folder
2. Open [Claude Chat](https://claude.ai)
3. Create a new **Project** (or open an existing one)
4. Upload the `.skill` file to the project's knowledge base
5. Start a conversation -- Claude will automatically apply the skill when relevant

> **Tip:** `.skill` files are ZIP archives containing a `SKILL.md` inside a named folder. You can also unzip them and read the markdown directly if you want to review or customize the instructions before uploading.

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
2. **Update the Coda schema** (or replace Coda with your own tool -- Notion, Airtable, etc.)
3. **Edit the `CLAUDE.md`** pipeline spec to match your workflow steps
4. **Update the `SKILL.md`** trigger phrases and processing logic
5. **Replace the Python scripts** with your own API integrations if needed

### General Principles

- **Skills are just structured prompts.** There is no magic -- every skill is a markdown file that tells Claude what to do, in what order, and in what format.
- **Start by copying, then customize.** It is easier to edit an existing skill than to write one from scratch.
- **Test in draft mode first.** Use `--dry-run` flags (where available) or set pipeline mode to `TEST` before going to production.
- **Keep sensitive data out of skills.** API keys go in `.env` files, never in skill definitions or prompts.

---

<p align="center">
  <sub>Built with Claude Code &bull; Questions? Reach out to Brady Redfearn in Program Development</sub>
</p>
