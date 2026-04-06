"""
beast_to_coda.py
----------------
Reads a 10-column BEAST import CSV from stdin and upserts changed/new rows
to the Coda To Do List table using Task ID as the upsert key.

Import columns (in order): Task ID, Name, Status, Priority, Due Date,
Type, Project, Effort, Notes, Link

Usage:
    cat import.csv | python scripts/beast_to_coda.py
    cat import.csv | python scripts/beast_to_coda.py --dry-run
    cat import.csv | python scripts/beast_to_coda.py --verbose
"""

import csv
import io
import re
import sys
from datetime import datetime

from coda_client import CodaClient

# BEAST table
BEAST_TABLE_ID = "grid-M-DmPD4U5x"
TASK_ID_COL = "c-ImEDreEoEA"

# Import column order: column display name -> Coda column ID
IMPORT_COLUMNS = [
    ("Task ID",   "c-ImEDreEoEA"),
    ("Name",      "c-MBRsPfbd6d"),
    ("Status",    "c-zH_C1i-smP"),
    ("Priority",  "c-g-kRN3Y2aS"),
    ("Due Date",  "c-NP39SR6C8D"),
    ("Type",      "c-Z_PWA6_-Bb"),
    ("Project",   "c-W3gb8_ca2O"),
    ("Effort",    "c-RdNqDL9akn"),
    ("Notes",     "c-ioDsMHggmZ"),
    ("Link",      "c-wuGVeM0y7z"),
]

# Columns that must NEVER be in the import (Coda manages these)
FORBIDDEN_COLUMNS = {"Parent", "Subitems", "Calendar Week"}

# Strict validation for select fields
VALID_STATUS = {"Not started", "In progress", "Done", "Blocked"}
VALID_PRIORITY = {"High", "Medium", "Low"}
VALID_EFFORT = {"30 min", "Half day", "Full day", "Multi-day"}
VALID_TYPE = {"Action", "Meeting", "Research", "Deliverable", "Admin"}

# Known project names (warn on unknown, don't reject)
KNOWN_PROJECTS = {"Cicada", "Networking", "Team/Ops", "Onboarding",
                  "JFT SDP", "Learning Resources Analytics",
                  "Math Supplemental Content"}


def parse_date_to_iso(date_str):
    """Convert D Mon YYYY to ISO YYYY-MM-DD for the Coda API.

    Input:  '6 Apr 2026' or '13 Mar 2026'
    Output: '2026-04-06' or '2026-03-13'
    """
    if not date_str or not date_str.strip():
        return ""
    s = date_str.strip()
    # Already ISO format
    if re.match(r"^\d{4}-\d{2}-\d{2}", s):
        return s[:10]
    # Try D Mon YYYY
    try:
        dt = datetime.strptime(s, "%d %b %Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        pass
    # Try without zero-padding: parse manually
    match = re.match(r"^(\d{1,2})\s+(\w{3})\s+(\d{4})$", s)
    if match:
        try:
            dt = datetime.strptime(f"{int(match.group(1)):02d} {match.group(2)} {match.group(3)}", "%d %b %Y")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            pass
    print(f"  WARNING: Could not parse date '{s}', passing as-is.", file=sys.stderr)
    return s


def validate_row(row_dict):
    """Validate field values for a single row. Returns list of warnings."""
    warnings = []
    task_id = row_dict.get("Task ID", "").strip()

    if not task_id:
        return ["SKIP: No Task ID (child row)"]

    if not re.match(r"^BEAST-\d{4}$", task_id):
        warnings.append(f"Task ID '{task_id}' does not match BEAST-XXXX format")

    status = row_dict.get("Status", "").strip()
    if status and status not in VALID_STATUS:
        warnings.append(f"Invalid Status: '{status}'")

    priority = row_dict.get("Priority", "").strip()
    if priority and priority not in VALID_PRIORITY:
        warnings.append(f"Invalid Priority: '{priority}'")

    effort = row_dict.get("Effort", "").strip()
    if effort and effort not in VALID_EFFORT:
        warnings.append(f"Invalid Effort: '{effort}'")

    task_type = row_dict.get("Type", "").strip()
    if task_type and task_type not in VALID_TYPE:
        warnings.append(f"Invalid Type: '{task_type}'")

    project = row_dict.get("Project", "").strip()
    if project and project not in KNOWN_PROJECTS:
        warnings.append(f"Unknown Project: '{project}' (accepted, not in known list)")

    return warnings


def build_row_cells(row_dict):
    """Convert a CSV row dict to Coda cells list."""
    cells = []
    for col_name, col_id in IMPORT_COLUMNS:
        value = row_dict.get(col_name, "").strip()
        if not value:
            continue
        # Convert dates to ISO for Coda API
        if col_name == "Due Date":
            value = parse_date_to_iso(value)
        cells.append({"column": col_id, "value": value})
    return cells


def main():
    dry_run = "--dry-run" in sys.argv
    verbose = "--verbose" in sys.argv

    # Read CSV from --input file or stdin
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
        print("ERROR: No input received. Use --input <file> or pipe CSV via stdin.")
        sys.exit(1)

    reader = csv.DictReader(io.StringIO(raw))
    headers = reader.fieldnames or []

    # Validate headers
    expected = [col_name for col_name, _ in IMPORT_COLUMNS]
    for h in headers:
        if h in FORBIDDEN_COLUMNS:
            print(f"ERROR: Forbidden column '{h}' found in CSV. "
                  "Import CSV must not include Parent, Subitems, or Calendar Week.")
            sys.exit(1)

    rows = list(reader)

    if verbose or dry_run:
        print("=" * 60)
        print("BEAST TO CODA" + (" (DRY RUN)" if dry_run else ""))
        print("=" * 60)
        print(f"Table: Complete To Do List ({BEAST_TABLE_ID})")
        print(f"Input rows: {len(rows)}")
        print(f"CSV columns: {headers}")
        print()

    # Validate and build upsert payload
    valid_rows = []
    skip_count = 0
    error_count = 0

    for i, row in enumerate(rows):
        task_id = row.get("Task ID", "").strip()
        warnings = validate_row(row)

        if any(w.startswith("SKIP:") for w in warnings):
            skip_count += 1
            if verbose:
                print(f"  Row {i + 1}: SKIP (child row, no Task ID)")
            continue

        has_errors = any(
            w.startswith("Invalid") for w in warnings
        )

        if verbose:
            task_name = row.get("Name", "")[:50]
            print(f"  Row {i + 1}: {task_id} - {task_name}")
            for w in warnings:
                prefix = "ERROR" if w.startswith("Invalid") else "WARN"
                print(f"    {prefix}: {w}")

        if has_errors:
            error_count += 1
            print(f"  Row {i + 1} ({task_id}): REJECTED due to validation errors.",
                  file=sys.stderr)
            continue

        cells = build_row_cells(row)
        if cells:
            valid_rows.append({"cells": cells})

    print()
    print(f"Valid rows to upsert: {len(valid_rows)}")
    print(f"Skipped (child rows): {skip_count}")
    print(f"Rejected (errors): {error_count}")

    if not valid_rows:
        print("\nNo valid rows to write.")
        return

    if dry_run:
        print("\nDRY RUN: No data written to Coda.")
        return

    # Upsert using Task ID as the key column
    client = CodaClient(verbose=verbose)
    result = client.upsert_rows(BEAST_TABLE_ID, valid_rows, [TASK_ID_COL])

    request_id = result.get("requestId", "N/A")
    print(f"\nSUCCESS: Upsert request accepted.")
    print(f"Request ID: {request_id}")


if __name__ == "__main__":
    main()
