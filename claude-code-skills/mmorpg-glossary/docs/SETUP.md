# MMORPG Glossary Tool -- Setup Guide

**MMORPG** = Massively Multi-employee Online Reference for Programs Glossary

A tool for searching, adding, editing, and deleting WGU glossary terms stored in a Coda table. Includes Python scripts for Coda API access and a Claude Code plugin for conversational interaction.

**Current status:** The Claude Code plugin trigger is unreliable. The Python scripts work correctly and can be run directly. A web-based interface is planned as a future improvement.

## Prerequisites

- **Python 3.10+** installed
- **Coda API key** with access to the glossary document
- **Git** (to clone this repo)
- **Claude Code** (optional, for the conversational plugin)

## Step 1: Clone the Repo

```bash
git clone https://github.com/brady-wgu/claude_skills.git
cd claude_skills/claude-code-skills/mmorpg-glossary
```

## Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs two packages: `requests` (HTTP client) and `python-dotenv` (environment variable loader).

## Step 3: Configure Your Coda API Key

1. Copy the example config:
   ```bash
   cp config.example.env .env
   ```

2. Open `.env` in a text editor and replace the placeholder with your actual Coda API key:
   ```
   CODA_API_KEY=your-actual-key-here
   CODA_DOC_ID=dHXfr0V468
   ```

   To get a Coda API key: go to https://coda.io/account, scroll to "API Settings", and generate a new token.

3. Verify connectivity:
   ```bash
   python scripts/cli.py discover
   ```
   You should see the Glossary table ID and column IDs. If you get an auth error, double-check your API key.

## Using the Scripts Directly

The Python scripts are the reliable interface. Run from the project root:

| Command | What it does |
|---------|-------------|
| `python scripts/cli.py list` | List all glossary terms (JSON output) |
| `python scripts/cli.py search "SDP"` | Search across all columns for a term |
| `python scripts/cli.py add --term "X" --full-name "Y" --definition "Z"` | Add a new term (warns on duplicates) |
| `python scripts/cli.py edit --term "X" --definition "new text"` | Edit an existing term |
| `python scripts/cli.py delete --term "X"` | Delete a term |
| `python scripts/cli.py dump` | Export full glossary as JSON |
| `python scripts/cli.py discover` | Show Coda table and column IDs |

All write commands support `--dry-run` to preview without writing. All commands support `--verbose` for API debugging.

## Claude Code Plugin (Experimental)

The plugin provides a conversational interface so you can ask questions like "Search my glossary for assessment" instead of running scripts manually. Plugin triggering is currently unreliable, so this is considered experimental.

### Installing the Plugin

Copy the `plugin/` directory to your Claude Code plugins folder:

**Windows:**
```bash
xcopy /E /I plugin "%USERPROFILE%\.claude\plugins\mmorpg-glossary"
```

**Mac/Linux:**
```bash
cp -r plugin/ ~/.claude/plugins/mmorpg-glossary
```

Restart Claude Code for the plugin to load.

### Update the Script Path

1. Open `~/.claude/plugins/mmorpg-glossary/skills/glossary/SKILL.md`
2. Find the line: `All scripts run from: C:\Users\brady.redfearn\Projects\mmorpg-glossary`
3. Replace it with your actual path

### Trigger Words

Include one of these words in your request to help Claude recognize it as a glossary request:

| Trigger Word | Example |
|-------------|---------|
| **glossary** | "Search the glossary for assessment" |
| **my glossary** | "Check my glossary for SDP" |
| **brady's glossary** | "Look up UPL in brady's glossary" |
| **MMORPG** | "MMORPG: what does CQI stand for?" |

**Note:** Plain questions without a trigger word (e.g., "What does SDP mean?") will likely not trigger the glossary skill. Always include "glossary" or similar.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "CODA_API_KEY not set" | Check that `.env` exists and has your key |
| "Could not find table named 'Glossary'" | Run `python scripts/cli.py discover` to see available tables |
| Auth errors (401/403) | Regenerate your Coda API key at https://coda.io/account |
| Plugin not triggering | Include "glossary" in your request. Verify plugin folder exists at `~/.claude/plugins/mmorpg-glossary/`. Restart Claude Code. If still failing, use the scripts directly. |
| Stale data after add/edit | Coda has a few seconds of propagation delay; retry the search |

## Glossary Schema

The glossary table has four columns:

| Column | Required | Description |
|--------|----------|-------------|
| Term | Yes | The abbreviation or short name (e.g., "SDP", "UPL") |
| Full Name | No | The expanded name (e.g., "Skills Development Platform") |
| Definition | No | Free-text definition; can be multi-paragraph |
| Source | No | Origin of the term (e.g., "WGU Master Glossary" or blank) |

## Future Plans

A web-based interface is planned to replace the Claude Code plugin, making the glossary accessible to colleagues through a browser without any setup.
