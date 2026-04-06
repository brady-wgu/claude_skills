# Setup Guide

## Prerequisites

- Python 3.10 or later
- Git
- Claude Code installed and authenticated
- A Coda API key with access to Brady's Coda Playground

## Installation

1. Clone the repository:

   git clone <repo-url>
   cd blog-beast-automation

2. Install Python dependencies:

   pip install -r requirements.txt

3. Create your environment file:

   Copy config.example.env to .env and add your Coda API key.
   Never commit .env to version control.

4. Verify Coda connectivity:

   python scripts/coda_client.py --discover

   This lists all tables and columns in the doc. Confirm the Daily Log
   and Complete To Do List tables are present.

## Daily Usage

1. Open Claude Code in the blog-beast-automation directory
2. Paste your raw daily work notes
3. Claude processes BLOG, writes to Coda, pulls BEAST, processes BEAST,
   writes updates back to Coda, and produces a final report
4. In TEST mode, you confirm each step before it proceeds
5. Review the final report for sensitive items and today's priority list

## Switching Modes

Edit the MODE line in CLAUDE.md:

   MODE: TEST        (pause after every step)
   MODE: PRODUCTION  (run straight through)

## Scripts Reference

coda_client.py --discover [--verbose]
   List all tables and column schemas in the Coda doc.

blog_to_coda.py [--dry-run] [--verbose]
   Reads BLOG JSON from stdin, writes to Daily Log table.
   Strips markdown to plain text for Coda API compatibility.

beast_from_coda.py [--verbose]
   Pulls BEAST table, outputs 12-column CSV to stdout.
   Dates converted from ISO to D Mon YYYY format.

beast_to_coda.py [--dry-run] [--verbose]
   Reads 10-column import CSV from stdin, upserts to BEAST table.
   Validates field values, converts dates to ISO for API.

## Troubleshooting

401 Unauthorized:
   Regenerate your Coda API key at https://coda.io/account#apiSettings
   and update .env.

Doc ID mismatch:
   The scripts are scoped to doc dHXfr0V468. If you need a different
   doc, update ALLOWED_DOC_ID in coda_client.py and CODA_DOC_ID in .env.

Formatting not rendering in Coda:
   Coda's API does not render markdown or HTML in table cells. All text
   is written as plain text. This is a known Coda platform limitation.
