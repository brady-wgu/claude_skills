---
name: glossary-lookup
model: sonnet
description: >
  Search, add, edit, delete, and query WGU glossary terms stored in Coda. Use this skill when
  the user asks about WGU terminology, acronyms, definitions, or the glossary. Trigger phrases
  include: "what does X mean", "what does X stand for", "define X", "glossary", "look up",
  "MMORPG", "add to glossary", "update glossary", "delete from glossary", "search glossary",
  "list all terms", "what is the difference between X and Y", or any question about WGU
  institutional vocabulary, roles, systems, or acronyms.
---

# MMORPG Glossary Tool

MMORPG = Massively Multi-employee Online Reference for Programs Glossary

This skill provides conversational access to Brady's WGU glossary stored in Coda. All data lives in the Glossary table in Brady's Coda Playground (doc ID dHXfr0V468). Coda is the single source of truth.

## Project Location

All scripts run from: `C:\Users\brady.redfearn\Projects\mmorpg-glossary`

## How to Execute Commands

Run all commands via Bash from the project root:

```
cd C:\Users\brady.redfearn\Projects\mmorpg-glossary && python scripts/cli.py <command> [args]
```

All commands output JSON. Parse the JSON to formulate your response.

## Available Commands

### Search for a term
```
python scripts/cli.py search "<query>"
```
Returns all entries where any field (Term, Full Name, Definition, Source) contains the query as a case-insensitive substring. Results are sorted alphabetically.

### List all terms
```
python scripts/cli.py list
```
Returns all glossary entries sorted alphabetically. Use sparingly (292+ entries).

### Add a new term
```
python scripts/cli.py add --term "<TERM>" --full-name "<Full Name>" --definition "<Definition text>" --source "<Source>"
```
Only `--term` is required. Other fields are optional.

If the term already exists, the command returns a `duplicate_warning` status with the existing entries. Ask the user if they want to add anyway. If yes, re-run with `--force`:
```
python scripts/cli.py add --term "<TERM>" --definition "<text>" --force
```

### Edit an existing term
```
python scripts/cli.py edit --term "<TERM>" --definition "<new definition>"
```
Supported update flags: `--full-name`, `--definition`, `--source`, `--new-term` (to rename).

If multiple entries share the same term (like "AS"), the command returns an `ambiguous` status with all matches. Present them to the user numbered. Once the user picks one, re-run with the specific row ID:
```
python scripts/cli.py edit --term "<TERM>" --row-id "<row_id>" --definition "<new text>"
```

### Delete a term
```
python scripts/cli.py delete --term "<TERM>"
```
ALWAYS confirm with the user before running delete. If ambiguous (multiple matches), present the matches and use `--row-id`:
```
python scripts/cli.py delete --term "<TERM>" --row-id "<row_id>"
```

### Dump full glossary (for complex questions)
```
python scripts/cli.py dump
```
Returns all entries as JSON. Use this when the user asks a comparative or analytical question that requires seeing multiple entries together (e.g., "What's the difference between CQI and UPL?" or "List all assessment-related terms").

### Discover table schema
```
python scripts/cli.py discover
```
Shows table ID and column IDs. Use only for debugging.

## Response Guidelines

- Present results conversationally, not as raw JSON
- For lookups: state the term, full name, and definition clearly
- For multi-meaning terms: present all meanings, numbered, with full names
- For search results: list matches in a clean format (term, full name, brief definition)
- For add/edit/delete: confirm what was done
- If a term is not found: say so and suggest adding it
- For comparative questions ("what's the difference between X and Y"): search for both terms and compare their definitions
- No em dashes in output
- No AI cliches ("delve", "dive into", "it's important to note", "landscape", "let's unpack")
- Professional tone, concise and direct
- Coda propagation delay: after add/edit/delete, the change may take a few seconds to appear in subsequent searches. If a search right after a write returns stale data, wait 5 seconds and retry once.

## Examples

**User:** "What does SDP stand for?"
**Action:** Run `search "SDP"`, present the result conversationally.

**User:** "Add MMORPG to the glossary"
**Action:** Ask for full name and definition if not provided. Run `add` command. Confirm creation.

**User:** "What's the difference between EPD and PDO?"
**Action:** Run `dump`, find both entries in the JSON, compare their definitions in the response.

**User:** "Delete the test entry"
**Action:** Run `search "test"` to find it. Confirm with user before running `delete`.

**User:** "Show me all assessment-related terms"
**Action:** Run `search "assessment"`, present the results as a formatted list.
