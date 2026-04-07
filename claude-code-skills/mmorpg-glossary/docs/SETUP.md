# MMORPG Glossary Tool -- Setup Guide

**MMORPG** = Massively Multi-employee Online Reference for Programs Glossary

A conversational tool for searching, adding, editing, and deleting WGU glossary terms. You interact with it through Claude Code using natural language. The glossary data lives in Coda.

## Prerequisites

- **Claude Code** installed and configured (CLI, Desktop, or IDE)
- **Python 3.10+** installed
- **Coda API key** with access to the glossary document
- **Git** (to clone this repo)

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

## Step 4: Install the Claude Code Plugin

Copy the `plugin/` directory to your Claude Code plugins folder:

**Windows:**
```bash
xcopy /E /I plugin "%USERPROFILE%\.claude\plugins\mmorpg-glossary"
```

**Mac/Linux:**
```bash
cp -r plugin/ ~/.claude/plugins/mmorpg-glossary
```

Restart Claude Code (or start a new session) for the plugin to load.

## Step 5: Update the Script Path

The SKILL.md file references scripts at a specific path. Update the path in the SKILL.md to match where you cloned the repo:

1. Open `~/.claude/plugins/mmorpg-glossary/skills/glossary-lookup/SKILL.md`
2. Find the line: `All scripts run from: C:\Users\brady.redfearn\Projects\mmorpg-glossary`
3. Replace it with your actual path, e.g.: `All scripts run from: /home/yourname/claude_skills/claude-code-skills/mmorpg-glossary`
4. Update the `cd` path in all command examples to match

## How to Use

Open Claude Code and ask about glossary terms. Include a **trigger word** so Claude knows to use the glossary tool instead of answering from general knowledge.

### Trigger Words

Any of these words or phrases will activate the glossary skill:

| Trigger | Example |
|---------|---------|
| **glossary** | "Search the glossary for assessment" |
| **my glossary** | "Check my glossary for SDP" |
| **brady's glossary** | "Look up UPL in brady's glossary" |
| **MMORPG** | "MMORPG: what does CQI stand for?" |
| **look up** | "Look up the definition of EPD" |
| **define** | "Define SDP from the glossary" |

### Example Requests

**Searching and looking up terms:**
- "Glossary: what does SDP stand for?"
- "Search my glossary for assessment"
- "Look up UPL in the glossary"

**Adding new terms:**
- "Add MMORPG to the glossary: Massively Multi-employee Online Reference for Programs Glossary"
- "Glossary: add a new term for XYZ"

**Editing existing terms:**
- "Update the definition of CQI in the glossary"
- "Glossary: change the full name of SDP"

**Deleting terms:**
- "Delete the test entry from the glossary"

**Comparing terms:**
- "Glossary: what's the difference between EPD and PDO?"

**Listing everything:**
- "List all terms in my glossary"

### Why Trigger Words Matter

Without a trigger word, Claude may answer from general knowledge instead of consulting the Coda glossary. For example:

- "What does SDP mean?" -- Claude may answer from general knowledge (not reliable)
- "Glossary: what does SDP mean?" -- Claude uses the glossary tool (reliable)

The simplest habit: start your request with "glossary:" or include "my glossary" somewhere in the sentence.

Claude handles the Coda API calls behind the scenes. You never need to run Python commands yourself.

## Model Requirement

The skill runs on **Sonnet 4.6 or above**. If you are using a lighter model, Claude will tell you to switch.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "CODA_API_KEY not set" | Check that `.env` exists and has your key |
| "Could not find table named 'Glossary'" | Run `python scripts/cli.py discover` to see available tables |
| Auth errors (401/403) | Regenerate your Coda API key at https://coda.io/account |
| Skill not triggering | Include a trigger word like "glossary" or "my glossary" in your request. Also check that the plugin folder exists at `~/.claude/plugins/mmorpg-glossary/` and restart Claude Code |
| Stale data after add/edit | Coda has a few seconds of propagation delay; retry the search |

## Glossary Schema

The glossary table has four columns:

| Column | Required | Description |
|--------|----------|-------------|
| Term | Yes | The abbreviation or short name (e.g., "SDP", "UPL") |
| Full Name | No | The expanded name (e.g., "Skills Development Platform") |
| Definition | No | Free-text definition; can be multi-paragraph |
| Source | No | Origin of the term (e.g., "WGU Master Glossary" or blank) |
