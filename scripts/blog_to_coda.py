"""
blog_to_coda.py
---------------
Reads structured BLOG output as JSON from stdin and creates a new row
in the Coda Daily Log table.

Section 7 (Sensitive Items) is NEVER included in the write.

Usage:
    echo '{"date": "06 Apr 2026", ...}' | python scripts/blog_to_coda.py
    echo '{"date": "06 Apr 2026", ...}' | python scripts/blog_to_coda.py --dry-run
    echo '{"date": "06 Apr 2026", ...}' | python scripts/blog_to_coda.py --verbose
"""

import json
import re
import sys

from coda_client import CodaClient

# Daily Log table
LOG_TABLE_ID = "grid-ty2WGfh4qa"

# Column mapping: JSON key -> Coda column ID
LOG_COLUMNS = {
    "date":             "c-oiaBDBstH1",
    "reviewed_notes":   "c-DXM4h2B28G",
    "polished_summary": "c-FIWz6AEhwd",
    "executive_bullets": "c-WSCAvrHbnz",
    "key_wins":         "c-QuKWx0lwGp",
    "blockers":         "c-bT-C79ocGH",
    "category":         "c-CA6Nwa3A2N",
    "status":           "c-pR0VmtQ5AV",
    "entry_type":       "c-7IZ-UJNjXG",
}

# Fields that contain prose and need markdown stripped for Coda plain text
PROSE_FIELDS = {
    "reviewed_notes", "polished_summary", "executive_bullets",
    "key_wins", "blockers",
}

# These keys must never appear in the payload
FORBIDDEN_KEYS = {"sensitive_items", "section_7"}


def strip_markdown(text):
    """Strip markdown formatting to clean plain text for Coda API.

    Coda's API does not render markdown or HTML in cell writes.
    This converts markdown to readable plain text:
    - ### Heading -> HEADING (uppercase, standalone line)
    - **bold text** -> bold text (markers removed)
    - - bullet item -> bullet item (dash preserved, readable as plain text)
    """
    lines = text.split("\n")
    result = []
    for line in lines:
        stripped = line.strip()

        # Convert ### Heading to uppercase plain text
        heading_match = re.match(r"^#{1,3}\s+(.+)$", stripped)
        if heading_match:
            result.append(heading_match.group(1).strip().upper())
            continue

        # Strip **bold** markers
        line = re.sub(r"\*\*(.+?)\*\*", r"\1", line)

        result.append(line)
    return "\n".join(result)


def build_cells(data):
    """Convert JSON input to Coda cells list. Validates and maps fields."""
    cells = []

    for key in list(FORBIDDEN_KEYS):
        if key in data:
            print(f"WARNING: '{key}' found in input. Removing. Sensitive items are NEVER written to Coda.")
            del data[key]

    # Always set entry_type and status
    data.setdefault("entry_type", "Daily")
    data.setdefault("status", "Draft")

    # Strip markdown formatting for Coda plain text API
    for field in PROSE_FIELDS:
        if field in data and data[field]:
            data[field] = strip_markdown(data[field])

    for json_key, col_id in LOG_COLUMNS.items():
        value = data.get(json_key)
        if value is not None and str(value).strip():
            cells.append({"column": col_id, "value": str(value).strip()})

    return cells


def main():
    dry_run = "--dry-run" in sys.argv
    verbose = "--verbose" in sys.argv

    # Read JSON from --input file or stdin
    input_file = None
    for i, arg in enumerate(sys.argv):
        if arg == "--input" and i + 1 < len(sys.argv):
            input_file = sys.argv[i + 1]

    if input_file:
        with open(input_file, "r", encoding="utf-8") as f:
            raw = f.read().strip()
    else:
        raw = sys.stdin.read().strip()

    if not raw:
        print("ERROR: No input received. Use --input <file> or pipe JSON via stdin.")
        sys.exit(1)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON on stdin: {e}")
        sys.exit(1)

    if not data.get("date"):
        print("ERROR: 'date' field is required in the JSON input.")
        sys.exit(1)

    cells = build_cells(data)

    if not cells:
        print("ERROR: No valid fields to write. Check JSON keys match expected fields.")
        print(f"Expected keys: {list(LOG_COLUMNS.keys())}")
        sys.exit(1)

    if verbose or dry_run:
        print("=" * 60)
        print("BLOG TO CODA" + (" (DRY RUN)" if dry_run else ""))
        print("=" * 60)
        print(f"Table: Daily Log ({LOG_TABLE_ID})")
        print(f"Fields to write ({len(cells)}):")
        for cell in cells:
            col_name = next(
                (k for k, v in LOG_COLUMNS.items() if v == cell["column"]), cell["column"]
            )
            val_preview = cell["value"][:80] + "..." if len(cell["value"]) > 80 else cell["value"]
            print(f"  {col_name}: {val_preview}")
        print()

    if dry_run:
        print("DRY RUN: No data written to Coda.")
        payload = {"rows": [{"cells": cells}]}
        print(f"\nPayload that would be sent:\n{json.dumps(payload, indent=2)}")
        return

    client = CodaClient(verbose=verbose)
    result = client.create_row(LOG_TABLE_ID, cells)

    request_id = result.get("requestId", "N/A")
    added = len(result.get("addedRowIds", []))

    print(f"SUCCESS: {added} row(s) created in Daily Log.")
    print(f"Request ID: {request_id}")
    if result.get("addedRowIds"):
        print(f"Row ID: {result['addedRowIds'][0]}")


if __name__ == "__main__":
    main()
