"""
beast_from_coda.py
------------------
Pulls the Complete To Do List (BEAST) table from Coda and outputs a
12-column CSV to stdout for BEAST processing.

Columns (in order): Task ID, Name, Status, Priority, Due Date, Type,
Project, Effort, Notes, Link, Parent, Subitems

Usage:
    python scripts/beast_from_coda.py
    python scripts/beast_from_coda.py --verbose
"""

import csv
import io
import os
import re
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from coda_client import CodaClient
from pipeline_config import load_config

# Load table/column IDs from config.json (or hardcoded defaults)
_config = load_config()
BEAST_TABLE_ID = _config["beast_table_id"]
_beast_cols = _config["beast_columns"]

# Export column order: column display name -> Coda column ID
# All 12 columns including Parent and Subitems for full context
EXPORT_COLUMN_NAMES = [
    "Task ID", "Name", "Status", "Priority", "Due Date", "Type",
    "Project", "Effort", "Notes", "Link", "Parent", "Subitems",
]
EXPORT_COLUMNS = [(name, _beast_cols[name]) for name in EXPORT_COLUMN_NAMES if name in _beast_cols]


DUE_DATE_COL = _beast_cols.get("Due Date", "c-NP39SR6C8D")


def format_date(value):
    """Convert ISO date to BEAST format: D Mon YYYY (no zero-padding).

    Input:  '2026-04-06T00:00:00.000-04:00' or '2026-04-06'
    Output: '6 Apr 2026'
    """
    if not value:
        return ""
    s = str(value).strip()
    # Try ISO with time
    match = re.match(r"(\d{4})-(\d{2})-(\d{2})", s)
    if match:
        dt = datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        # D Mon YYYY, no zero-padding: use %-d on Linux, %#d on Windows
        try:
            return dt.strftime("%-d %b %Y")
        except ValueError:
            return dt.strftime("%#d %b %Y")
    return s


def format_cell(value, col_id=None):
    """Convert a Coda cell value to a clean string for CSV output."""
    if value is None:
        return ""
    if col_id == DUE_DATE_COL:
        return format_date(value)
    if isinstance(value, list):
        # Lookup columns (Parent, Subitems) return lists of linked row names
        return "; ".join(str(v) for v in value)
    return str(value).strip()


def main():
    verbose = "--verbose" in sys.argv

    client = CodaClient(verbose=verbose)
    rows = client.get_rows(BEAST_TABLE_ID)

    if verbose:
        print(f"Fetched {len(rows)} row(s) from BEAST table.", file=sys.stderr)

    # Write CSV to stdout
    output = io.StringIO()
    writer = csv.writer(output)

    # Header row
    writer.writerow([col_name for col_name, _ in EXPORT_COLUMNS])

    # Data rows
    for row in rows:
        values = row.get("values", {})
        csv_row = []
        for col_name, col_id in EXPORT_COLUMNS:
            csv_row.append(format_cell(values.get(col_id), col_id))
        writer.writerow(csv_row)

    print(output.getvalue(), end="")

    if verbose:
        # Count parent vs child rows
        task_id_col = _beast_cols.get("Task ID", "c-ImEDreEoEA")
        parent_count = sum(
            1 for r in rows
            if r.get("values", {}).get(task_id_col)
        )
        child_count = len(rows) - parent_count
        print(f"Parent rows (with Task ID): {parent_count}", file=sys.stderr)
        print(f"Child rows (no Task ID): {child_count}", file=sys.stderr)


if __name__ == "__main__":
    main()
