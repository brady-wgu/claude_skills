"""
glossary_service.py
-------------------
Business logic for glossary CRUD operations against Coda.
Discovers the Glossary table and column IDs at startup, then provides
fetch, search, add, edit, delete, and dump operations.
"""

import json
import sys

from scripts.coda_client import CodaClient


class GlossaryService:
    TABLE_NAME = "Glossary"
    EXPECTED_COLUMNS = {"Term", "Full Name", "Definition", "Source"}

    def __init__(self, verbose=False):
        self.client = CodaClient(verbose=verbose)
        self.verbose = verbose
        self.table_id = self._discover_table()
        self.columns = self._discover_columns()

    def _discover_table(self):
        tables = self.client.list_tables()
        for t in tables:
            if t.get("name", "").strip().lower() == self.TABLE_NAME.lower():
                if self.verbose:
                    print(f"Found table '{t['name']}' -> {t['id']}", file=sys.stderr)
                return t["id"]
        available = [t.get("name", "?") for t in tables]
        raise RuntimeError(
            f"Could not find table named '{self.TABLE_NAME}'. "
            f"Available tables: {', '.join(available)}"
        )

    def _discover_columns(self):
        schema = self.client.get_table_schema(self.table_id)
        col_map = {}
        for col in schema:
            name = col.get("name", "")
            col_id = col.get("id", "")
            if name in self.EXPECTED_COLUMNS:
                col_map[name] = col_id
                if self.verbose:
                    print(f"  Column '{name}' -> {col_id}", file=sys.stderr)
        missing = self.EXPECTED_COLUMNS - set(col_map.keys())
        if missing:
            print(
                f"WARNING: Missing expected columns: {', '.join(missing)}",
                file=sys.stderr,
            )
        return col_map

    def discover(self):
        result = {
            "table_name": self.TABLE_NAME,
            "table_id": self.table_id,
            "columns": self.columns,
        }
        return result

    def _parse_row(self, row):
        values = row.get("values", {})
        term_col = self.columns.get("Term", "")
        fullname_col = self.columns.get("Full Name", "")
        def_col = self.columns.get("Definition", "")
        source_col = self.columns.get("Source", "")

        term = str(values.get(term_col, "")).strip()
        if not term:
            return None

        return {
            "row_id": row.get("id", ""),
            "term": term,
            "full_name": str(values.get(fullname_col, "")).strip(),
            "definition": str(values.get(def_col, "")).strip(),
            "source": str(values.get(source_col, "")).strip(),
        }

    def fetch_all(self):
        raw_rows = self.client.get_rows(self.table_id)
        parsed = []
        for row in raw_rows:
            entry = self._parse_row(row)
            if entry:
                parsed.append(entry)
        parsed.sort(key=lambda r: r["term"].lower())
        return parsed

    def search(self, query):
        query_lower = query.lower()
        results = []
        for entry in self.fetch_all():
            searchable = " ".join([
                entry["term"],
                entry["full_name"],
                entry["definition"],
                entry["source"],
            ]).lower()
            if query_lower in searchable:
                results.append(entry)
        results.sort(key=lambda r: r["term"].lower())
        return results

    def add_term(self, term, full_name="", definition="", source=""):
        existing = self.fetch_all()
        dupes = [e for e in existing if e["term"].lower() == term.lower()]

        cells = []
        if "Term" in self.columns:
            cells.append({"column": self.columns["Term"], "value": term})
        if full_name and "Full Name" in self.columns:
            cells.append({"column": self.columns["Full Name"], "value": full_name})
        if definition and "Definition" in self.columns:
            cells.append({"column": self.columns["Definition"], "value": definition})
        if source and "Source" in self.columns:
            cells.append({"column": self.columns["Source"], "value": source})

        if dupes:
            return {
                "status": "duplicate_warning",
                "existing": dupes,
                "message": f"Term '{term}' already exists ({len(dupes)} match(es)). "
                           "Use --force to add anyway.",
                "cells": cells,
            }

        result = self.client.create_row(self.table_id, cells)
        return {"status": "created", "response": result}

    def add_term_force(self, term, full_name="", definition="", source=""):
        cells = []
        if "Term" in self.columns:
            cells.append({"column": self.columns["Term"], "value": term})
        if full_name and "Full Name" in self.columns:
            cells.append({"column": self.columns["Full Name"], "value": full_name})
        if definition and "Definition" in self.columns:
            cells.append({"column": self.columns["Definition"], "value": definition})
        if source and "Source" in self.columns:
            cells.append({"column": self.columns["Source"], "value": source})

        result = self.client.create_row(self.table_id, cells)
        return {"status": "created", "response": result}

    def edit_term(self, term, updates):
        existing = self.fetch_all()
        matches = [e for e in existing if e["term"].lower() == term.lower()]

        if not matches:
            return {"status": "not_found", "message": f"No term matching '{term}' found."}

        if len(matches) > 1:
            return {
                "status": "ambiguous",
                "matches": matches,
                "message": f"Multiple entries match '{term}'. Specify by row_id.",
            }

        cells = []
        field_map = {
            "term": "Term",
            "full_name": "Full Name",
            "definition": "Definition",
            "source": "Source",
        }

        target = matches[0]
        cells.append({"column": self.columns["Term"], "value": target["term"]})

        for field_key, new_value in updates.items():
            col_name = field_map.get(field_key, field_key)
            if col_name in self.columns:
                cells.append({"column": self.columns[col_name], "value": new_value})

        rows = [{"cells": cells}]
        result = self.client.upsert_rows(
            self.table_id, rows, [self.columns["Term"]]
        )
        return {"status": "updated", "response": result}

    def edit_term_by_row_id(self, row_id, updates):
        all_rows = self.fetch_all()
        target = None
        for entry in all_rows:
            if entry["row_id"] == row_id:
                target = entry
                break

        if not target:
            return {"status": "not_found", "message": f"No row with ID '{row_id}' found."}

        cells = []
        field_map = {
            "term": "Term",
            "full_name": "Full Name",
            "definition": "Definition",
            "source": "Source",
        }

        cells.append({"column": self.columns["Term"], "value": target["term"]})

        for field_key, new_value in updates.items():
            col_name = field_map.get(field_key, field_key)
            if col_name in self.columns:
                cells.append({"column": self.columns[col_name], "value": new_value})

        rows = [{"cells": cells}]
        result = self.client.upsert_rows(
            self.table_id, rows, [self.columns["Term"]]
        )
        return {"status": "updated", "response": result}

    def delete_term(self, term):
        existing = self.fetch_all()
        matches = [e for e in existing if e["term"].lower() == term.lower()]

        if not matches:
            return {"status": "not_found", "message": f"No term matching '{term}' found."}

        if len(matches) > 1:
            return {
                "status": "ambiguous",
                "matches": matches,
                "message": f"Multiple entries match '{term}'. Specify by row_id.",
            }

        target = matches[0]
        result = self.client.delete_row(self.table_id, target["row_id"])
        return {"status": "deleted", "term": target["term"], "response": result}

    def delete_term_by_row_id(self, row_id):
        all_rows = self.fetch_all()
        target = None
        for entry in all_rows:
            if entry["row_id"] == row_id:
                target = entry
                break

        if not target:
            return {"status": "not_found", "message": f"No row with ID '{row_id}' found."}

        result = self.client.delete_row(self.table_id, target["row_id"])
        return {"status": "deleted", "term": target["term"], "response": result}

    def dump(self):
        entries = self.fetch_all()
        return entries
