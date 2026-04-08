# Setup Guide

This guide walks you through setting up the blog-beast-pipeline skill so it runs end-to-end in Claude Code. The pipeline processes daily work notes, writes a structured journal entry to Coda, analyzes your task list, and syncs updates back to Coda -- all from a single command.

---

## Prerequisites

- Python 3.10 or later
- Git
- Claude Code installed and authenticated
- A Coda.io account with API access

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/brady-wgu/claude_skills.git
```

The pipeline lives at:
```
claude_skills/claude-code-skills/blog-beast-pipeline/
```

All paths below are relative to that directory.

---

## Step 2: Install Python Dependencies

```bash
cd claude_skills/claude-code-skills/blog-beast-pipeline
pip install -r requirements.txt
```

This installs `requests`, `python-dotenv`, and `truststore`. The `truststore` package allows Python to use the Windows system certificate store, which is required in corporate environments where a security proxy (e.g., zScaler) intercepts HTTPS traffic with its own root CA.

---

## Step 3: Configure Your Coda API Key

1. Go to https://coda.io/account#apiSettings and generate an API key
2. Copy `config.example.env` to `.env` in the same directory:
   ```bash
   cp config.example.env .env
   ```
3. Edit `.env` and replace the placeholder with your actual key:
   ```
   CODA_API_KEY=your-actual-coda-api-key
   CODA_DOC_ID=dHXfr0V468
   ```

**Important:** The `.env` file must live in the `blog-beast-pipeline/` directory (next to `CLAUDE.md`). The scripts resolve this path automatically. Never commit `.env` to version control.

---

## Step 4: Configure Your Coda Document

The pipeline is scoped to a specific Coda document. Out of the box, it points to Brady's Coda Playground (`dHXfr0V468`). To use your own document:

1. Create a Coda doc with two tables:
   - **Daily Log** -- for BLOG journal entries (columns: Date, Reviewed Notes, Polished Summary, Executive Bullets, Key Wins, Blockers, Category, Status, Entry Type)
   - **Complete To Do List** -- for BEAST task tracking (columns: Task ID, Name, Status, Priority, Due Date, Type, Project, Effort, Notes, Link, Parent, Subitems)

2. Get your doc ID from the Coda URL (the string after `/d/` in `https://coda.io/d/Your-Doc-Name_dXXXXXXXXX`)

3. Update two files:
   - `.env`: set `CODA_DOC_ID` to your doc ID
   - `scripts/coda_client.py`: update `ALLOWED_DOC_ID` on line 35 to match your doc ID (this is a safety check that prevents writes to the wrong document)

---

## Step 5: Auto-Discover Your Coda Schema

Run the discovery script to find your table and column IDs automatically:

```bash
python scripts/discover_config.py
```

This connects to your Coda doc, finds tables named "Complete To Do List" and "Daily Log", maps all columns by name, and writes a `config.json` that all pipeline scripts load automatically.

If your tables have different names, update `BEAST_TABLE_NAME` and `LOG_TABLE_NAME` at the top of `scripts/discover_config.py`.

**Note:** If `config.json` does not exist, the scripts fall back to hardcoded defaults (Brady's workspace). This keeps the pipeline backwards-compatible for the original author.

---

## Step 6: Install the Claude Code Plugin

The plugin tells Claude Code how to run the pipeline when you say "run pipeline."

1. Copy the `plugin/` directory to your Claude Code plugins folder:
   ```bash
   cp -r plugin/ ~/.claude/plugins/brady-pipeline/
   ```
   On Windows:
   ```bash
   xcopy plugin\ %USERPROFILE%\.claude\plugins\brady-pipeline\ /E /I
   ```

2. Set `PIPELINE_DIR` in your `.env` file to the absolute path of the `blog-beast-pipeline/` directory. The skill plugin uses this variable in its `cd "$PIPELINE_DIR"` commands.

3. Restart Claude Code. The plugin will be loaded automatically.

---

## Step 7: Verify Everything Works

Run these checks from the `blog-beast-pipeline/` directory:

**Test Coda connectivity:**
```bash
python scripts/coda_client.py --discover
```
Should list your tables and columns.

**Test BLOG write (dry run):**
```bash
echo '{"date":"2026-01-01","reviewed_notes":"Test","polished_summary":"Test","executive_bullets":"Test","key_wins":"None","blockers":"None","category":"Admin","entry_type":"Daily","status":"Draft"}' > /tmp/test.json
python scripts/blog_to_coda.py --input /tmp/test.json --dry-run
```
Should show the payload without writing to Coda.

**Test BEAST pull:**
```bash
python scripts/beast_from_coda.py | head -5
```
Should show your task list as CSV.

**Test BEAST upsert (dry run):**
```bash
echo 'Task ID,Name,Status,Priority,Due Date,Type,Project,Effort,Notes,Link
BEAST-9999,Test task,Not started,Low,10 Apr 2026,Action,Team/Ops,30 min,Test,' > /tmp/test.csv
python scripts/beast_to_coda.py --input /tmp/test.csv --dry-run
```
Should validate the CSV without writing to Coda.

---

## Daily Usage

**Recommended model:** Sonnet at medium effort. The pipeline follows highly structured, rule-based instructions. Sonnet handles this efficiently. Opus is unnecessary and significantly slower. When triggered via the skill plugin, these settings are enforced automatically by the `model: sonnet` and `effort: medium` frontmatter fields in SKILL.md.

**Trigger phrases** -- any of these followed by pasted raw daily work notes:

| Trigger | When to Use |
|---------|-------------|
| `run pipeline` | Standard daily run (most common) |
| `run BLOG and BEAST` | Same as above, explicit |
| `run blog beast` | Shorthand |
| `process my notes` | Natural language alternative |
| `morning briefing` | When you want to emphasize the BEAST output |
| `run morning updates` | Same as above |
| `run BEAST` | Same -- the full pipeline always runs |
| `run BLOG` | Same -- the full pipeline always runs |
| `process today's notes` | Natural language alternative |

**Typical usage:**

1. Open Claude Code from any directory
2. Switch to **Sonnet** model if not already selected
3. Type `run pipeline:` followed by the date header and pasted raw daily work notes
4. Claude processes everything automatically and outputs a final report
5. Review the report for:
   - Sensitive items (displayed in terminal only, never written to Coda)
   - Today's priority list
   - Any new tasks that need Parent/Subitems manually assigned in Coda

---

## Pipeline Modes

Edit the MODE line in `plugin/skills/run-pipeline/SKILL.md`:

```
MODE: TEST        # Pause after every step for review
MODE: PRODUCTION  # Run straight through, output only the final report
```

---

## Scripts Reference

All scripts are in the `scripts/` directory and support `--verbose` for detailed logging.

| Script | Purpose | Key Flags |
|--------|---------|-----------|
| `discover_config.py` | Auto-discover Coda table/column IDs, write `config.json` | `--verbose` |
| `pipeline_config.py` | Shared config loader (imported by other scripts) | -- |
| `coda_client.py` | Coda API wrapper (scoped to one doc) | `--discover`, `--verbose` |
| `blog_to_coda.py` | Write BLOG entry to Daily Log table | `--input <file>`, `--dry-run`, `--verbose` |
| `beast_from_coda.py` | Pull BEAST table as 12-column CSV (stdout) | `--verbose` |
| `beast_to_coda.py` | Upsert BEAST import CSV to task table | `--input <file>`, `--dry-run`, `--verbose` |

---

## Troubleshooting

**401 Unauthorized:**
Regenerate your Coda API key at https://coda.io/account#apiSettings and update `.env`.

**Doc ID mismatch:**
The scripts are scoped to a specific doc via `ALLOWED_DOC_ID` in `coda_client.py`. Update both `coda_client.py` and `.env` if you change documents.

**Scripts can't find .env:**
The `.env` file must be in the `blog-beast-pipeline/` directory (one level above `scripts/`). The scripts resolve this path relative to their own location.

**Formatting not rendering in Coda:**
Coda's API does not render markdown or HTML in table cells. All text is written as plain text. This is a known Coda platform limitation. The scripts automatically strip markdown formatting before writing.

**SSL: CERTIFICATE_VERIFY_FAILED:**
This means Python cannot verify the Coda API's SSL certificate. Common in corporate environments where a security proxy (zScaler, Netskope, etc.) intercepts HTTPS with its own root CA. Fix: install `truststore` (`pip install truststore`). The scripts inject it automatically on import to use the OS certificate store instead of Python's bundled certifi CA bundle. If `truststore` is already installed and the error persists, check that your IT department has added the proxy's root CA to the Windows certificate store.

**Retryable errors (429, 502, 503, 504, timeouts):**
The scripts retry transient errors once automatically with a 3-second delay. If the error persists after the retry, the script exits with an error. Check your network connection and try again. For 429 (rate limit) errors, wait a minute before retrying.

**"run pipeline" doesn't trigger:**
Make sure the plugin is installed at `~/.claude/plugins/brady-pipeline/` and Claude Code has been restarted. As a fallback, open Claude Code directly in the `blog-beast-pipeline/` directory -- the `CLAUDE.md` there defines the same pipeline.
