# MMORPG Glossary Tool

CLI data layer for the MMORPG glossary skill. Provides CRUD access to the Glossary table in Brady's Coda Playground.

## Usage

All commands run from the project root. Output is JSON for Claude to parse.

    python scripts/cli.py discover
    python scripts/cli.py list
    python scripts/cli.py search "term"
    python scripts/cli.py add --term "X" --full-name "Y" --definition "Z" --source "S"
    python scripts/cli.py edit --term "X" --field "Definition" --value "new text"
    python scripts/cli.py delete --term "X"
    python scripts/cli.py dump

## Coda Schema

- Doc ID: dHXfr0V468
- Table: Glossary (ID discovered at runtime via API)
- Columns: Term, Full Name, Definition, Source

## Constraints

- Coda is the single source of truth. No local database, no caching.
- All reads pull live from Coda API. All writes go directly to Coda.
- Write commands support --dry-run. All commands support --verbose.
- Plain text only in Coda cells (no markdown, no HTML).

## Model Requirement

Minimum: Sonnet 4.6. The MMORPG skill runs on Sonnet or above.
