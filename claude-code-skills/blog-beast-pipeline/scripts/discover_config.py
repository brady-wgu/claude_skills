"""
discover_config.py
------------------
Auto-discovers Coda table and column IDs by name and writes config.json.

Run this once during setup. It connects to your Coda doc (using CODA_API_KEY
and CODA_DOC_ID from .env), finds tables by name, maps columns by name,
and writes a config.json that all pipeline scripts load automatically.

Usage:
    python scripts/discover_config.py
    python scripts/discover_config.py --verbose
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from coda_client import CodaClient

# Pipeline root = one directory up from scripts/
PIPELINE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(PIPELINE_ROOT, "config.json")

# ── Expected table and column names ─────────────────────────────────
# The discovery script matches by these names. If your Coda doc uses
# different table names, update them here.

BEAST_TABLE_NAME = "Complete To Do List"
LOG_TABLE_NAME = "Daily Log"

# Columns expected in the BEAST table (all 12, including Parent/Subitems)
BEAST_EXPECTED_COLUMNS = [
    "Task ID", "Name", "Status", "Priority", "Due Date", "Type",
    "Project", "Effort", "Notes", "Link", "Parent", "Subitems",
]

# Columns expected in the Daily Log table
LOG_EXPECTED_COLUMNS = [
    "Date", "Reviewed Notes", "Polished Summary", "Executive Bullets",
    "Key Wins", "Blockers", "Category", "Status", "Entry Type",
]


def find_table(tables, expected_name):
    """Find a table by name (case-insensitive). Returns (table_id, table_name) or None."""
    for t in tables:
        if t.get("name", "").strip().lower() == expected_name.lower():
            return t["id"], t["name"]
    return None, None


def map_columns(client, table_id, expected_columns):
    """Discover column IDs by name. Returns dict of {column_name: column_id}."""
    schema = client.get_table_schema(table_id)
    # Build name -> id lookup from Coda
    coda_columns = {col["name"]: col["id"] for col in schema}

    mapped = {}
    missing = []
    for col_name in expected_columns:
        if col_name in coda_columns:
            mapped[col_name] = coda_columns[col_name]
        else:
            missing.append(col_name)

    return mapped, missing, coda_columns


def main():
    verbose = "--verbose" in sys.argv

    print("=" * 60)
    print("PIPELINE CONFIG DISCOVERY")
    print("=" * 60)

    client = CodaClient(verbose=verbose)
    doc = client.get_doc()
    print(f"\nDoc: {doc.get('name', 'Unknown')}")
    print(f"Doc ID: {client.doc_id}")

    # ── Discover tables ──
    tables = client.list_tables()
    print(f"Found {len(tables)} table(s) in doc.")

    if verbose:
        for t in tables:
            print(f"  - {t.get('name', '?')} ({t.get('id', '?')})")

    beast_id, beast_name = find_table(tables, BEAST_TABLE_NAME)
    log_id, log_name = find_table(tables, LOG_TABLE_NAME)

    errors = []
    if not beast_id:
        errors.append(
            f"BEAST table not found. Expected name: \"{BEAST_TABLE_NAME}\"\n"
            f"  Available tables: {[t.get('name') for t in tables]}"
        )
    if not log_id:
        errors.append(
            f"Daily Log table not found. Expected name: \"{LOG_TABLE_NAME}\"\n"
            f"  Available tables: {[t.get('name') for t in tables]}"
        )

    if errors:
        print("\nERROR: Could not find required tables:")
        for e in errors:
            print(f"  {e}")
        print("\nUpdate BEAST_TABLE_NAME or LOG_TABLE_NAME in this script to match your Coda doc.")
        sys.exit(1)

    print(f"\nBEAST table: \"{beast_name}\" -> {beast_id}")
    print(f"Daily Log table: \"{log_name}\" -> {log_id}")

    # ── Discover columns ──
    print("\nMapping BEAST columns...")
    beast_cols, beast_missing, beast_all = map_columns(client, beast_id, BEAST_EXPECTED_COLUMNS)
    if beast_missing:
        print(f"  WARNING: Missing columns: {beast_missing}")
        print(f"  Available: {list(beast_all.keys())}")
    print(f"  Mapped {len(beast_cols)}/{len(BEAST_EXPECTED_COLUMNS)} columns.")

    print("\nMapping Daily Log columns...")
    log_cols, log_missing, log_all = map_columns(client, log_id, LOG_EXPECTED_COLUMNS)
    if log_missing:
        print(f"  WARNING: Missing columns: {log_missing}")
        print(f"  Available: {list(log_all.keys())}")
    print(f"  Mapped {len(log_cols)}/{len(LOG_EXPECTED_COLUMNS)} columns.")

    # ── Check for critical missing columns ──
    # These are required for the pipeline to function
    beast_critical = {"Task ID", "Name", "Status"}
    log_critical = {"Date"}
    beast_critical_missing = beast_critical - set(beast_cols.keys())
    log_critical_missing = log_critical - set(log_cols.keys())

    if beast_critical_missing or log_critical_missing:
        print(f"\nERROR: Critical columns missing:")
        if beast_critical_missing:
            print(f"  BEAST: {beast_critical_missing}")
        if log_critical_missing:
            print(f"  Daily Log: {log_critical_missing}")
        print("Cannot generate config. Fix your Coda table schema and re-run.")
        sys.exit(1)

    # ── Write config.json ──
    config = {
        "beast_table_id": beast_id,
        "log_table_id": log_id,
        "beast_columns": beast_cols,
        "log_columns": log_cols,
    }

    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    print(f"\nconfig.json written to: {CONFIG_PATH}")
    print("\n" + "=" * 60)
    print("DISCOVERY COMPLETE")
    print("=" * 60)
    print("\nYour pipeline is configured. You can now run the pipeline.")
    print("To re-discover (e.g., after schema changes): python scripts/discover_config.py")


if __name__ == "__main__":
    main()
