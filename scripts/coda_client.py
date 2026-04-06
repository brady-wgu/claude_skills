"""
coda_client.py
--------------
Low-level Coda API wrapper for blog-beast-automation.
Handles authentication, doc validation, table/column discovery, row reads, and row writes.

Safety: All operations are scoped to doc ID dHXfr0V468 only.
The ALLOWED_DOC_ID is hard-coded and validated on every instantiation.

Usage:
    python scripts/coda_client.py --discover    # List all tables and column schemas
"""

import json
import os
import sys

import requests
from dotenv import load_dotenv


class CodaClient:
    ALLOWED_DOC_ID = "dHXfr0V468"
    BASE_URL = "https://coda.io/apis/v1"

    def __init__(self, verbose=False):
        load_dotenv()
        self.api_key = os.getenv("CODA_API_KEY", "").strip()
        self.doc_id = os.getenv("CODA_DOC_ID", "").strip()
        self.verbose = verbose

        if not self.api_key:
            raise RuntimeError(
                "CODA_API_KEY not set. Copy config.example.env to .env and add your key."
            )

        if not self.doc_id:
            raise RuntimeError(
                "CODA_DOC_ID not set in .env. Expected: " + self.ALLOWED_DOC_ID
            )

        if self.doc_id != self.ALLOWED_DOC_ID:
            raise RuntimeError(
                f"CODA_DOC_ID mismatch. Expected {self.ALLOWED_DOC_ID}, got {self.doc_id}. "
                "This safety check prevents writes to the wrong document."
            )

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _get(self, path, params=None):
        url = f"{self.BASE_URL}{path}"
        if self.verbose:
            print(f"GET {url}")
            if params:
                print(f"  params: {params}")
        resp = requests.get(url, headers=self._headers(), params=params)
        resp.raise_for_status()
        data = resp.json()
        if self.verbose:
            print(f"  status: {resp.status_code}")
        return data

    def _post(self, path, body):
        url = f"{self.BASE_URL}{path}"
        if self.verbose:
            print(f"POST {url}")
            print(f"  body: {json.dumps(body, indent=2)}")
        resp = requests.post(url, headers=self._headers(), json=body)
        resp.raise_for_status()
        data = resp.json()
        if self.verbose:
            print(f"  status: {resp.status_code}")
            print(f"  response: {json.dumps(data, indent=2)}")
        return data

    def get_doc(self):
        """GET /docs/{docId} -- confirm connectivity and return doc metadata."""
        return self._get(f"/docs/{self.doc_id}")

    def list_tables(self):
        """GET /docs/{docId}/tables -- return all tables, handling pagination."""
        tables = []
        params = {"limit": 100}
        while True:
            data = self._get(f"/docs/{self.doc_id}/tables", params=params)
            tables.extend(data.get("items", []))
            next_token = data.get("nextPageToken")
            if not next_token:
                break
            params["pageToken"] = next_token
        return tables

    def get_table_schema(self, table_id):
        """GET /docs/{docId}/tables/{tableId}/columns -- return all columns."""
        columns = []
        params = {"limit": 100}
        while True:
            data = self._get(
                f"/docs/{self.doc_id}/tables/{table_id}/columns", params=params
            )
            columns.extend(data.get("items", []))
            next_token = data.get("nextPageToken")
            if not next_token:
                break
            params["pageToken"] = next_token
        return columns

    def get_rows(self, table_id, value_format="simpleWithArrays"):
        """GET /docs/{docId}/tables/{tableId}/rows -- return all rows, paginated."""
        rows = []
        params = {"limit": 200, "valueFormat": value_format}
        while True:
            data = self._get(
                f"/docs/{self.doc_id}/tables/{table_id}/rows", params=params
            )
            rows.extend(data.get("items", []))
            next_token = data.get("nextPageToken")
            if not next_token:
                break
            params["pageToken"] = next_token
        return rows

    def create_row(self, table_id, cells):
        """POST a single new row to a table.

        Args:
            table_id: The Coda table API ID.
            cells: List of dicts, each with 'column' (column ID) and 'value'.

        Returns:
            API response dict.
        """
        body = {
            "rows": [{"cells": cells}],
        }
        return self._post(f"/docs/{self.doc_id}/tables/{table_id}/rows", body)

    def upsert_rows(self, table_id, rows, key_columns):
        """POST rows with keyColumns for upsert behavior.

        Args:
            table_id: The Coda table API ID.
            rows: List of dicts, each with 'cells' (list of column/value dicts).
            key_columns: List of column IDs to use as upsert keys.

        Returns:
            API response dict (202 accepted for async processing).
        """
        body = {
            "rows": rows,
            "keyColumns": key_columns,
        }
        return self._post(f"/docs/{self.doc_id}/tables/{table_id}/rows", body)

    def discover(self):
        """List all tables and their full column schemas. Prints a formatted report."""
        print("=" * 60)
        print("CODA SCHEMA DISCOVERY")
        print("=" * 60)

        doc = self.get_doc()
        print(f"\nDoc: {doc.get('name', 'Unknown')}")
        print(f"Doc ID: {self.doc_id}")
        print(f"URL: {doc.get('browserLink', 'N/A')}")

        tables = self.list_tables()
        print(f"\nFound {len(tables)} table(s):\n")

        for table in tables:
            table_id = table.get("id", "")
            table_name = table.get("name", "Unknown")
            print("-" * 60)
            print(f"Table: {table_name}")
            print(f"  API ID: {table_id}")
            print(f"  Type: {table.get('tableType', 'N/A')}")

            columns = self.get_table_schema(table_id)
            print(f"  Columns ({len(columns)}):")
            for col in columns:
                col_id = col.get("id", "")
                col_name = col.get("name", "Unknown")
                col_type = col.get("format", {}).get("type", "unknown") if col.get("format") else "unknown"
                print(f"    {col_name}")
                print(f"      ID: {col_id}")
                print(f"      Type: {col_type}")
            print()

        print("=" * 60)
        print("DISCOVERY COMPLETE")
        print("=" * 60)


if __name__ == "__main__":
    if "--discover" in sys.argv:
        verbose = "--verbose" in sys.argv
        client = CodaClient(verbose=verbose)
        client.discover()
    else:
        print("Usage: python scripts/coda_client.py --discover [--verbose]")
        sys.exit(1)
