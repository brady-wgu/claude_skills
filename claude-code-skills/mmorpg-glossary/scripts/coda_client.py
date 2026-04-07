"""
coda_client.py
--------------
Low-level Coda API wrapper for the MMORPG glossary tool.
Handles authentication, doc validation, table/column discovery, row CRUD.

Safety: All operations are scoped to doc ID dHXfr0V468 only.
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
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env_path = os.path.join(project_root, ".env")
        load_dotenv(env_path)
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
            print(f"GET {url}", file=sys.stderr)
            if params:
                print(f"  params: {params}", file=sys.stderr)
        resp = requests.get(url, headers=self._headers(), params=params)
        resp.raise_for_status()
        data = resp.json()
        if self.verbose:
            print(f"  status: {resp.status_code}", file=sys.stderr)
        return data

    def _post(self, path, body):
        url = f"{self.BASE_URL}{path}"
        if self.verbose:
            print(f"POST {url}", file=sys.stderr)
            print(f"  body: {json.dumps(body, indent=2)}", file=sys.stderr)
        resp = requests.post(url, headers=self._headers(), json=body)
        resp.raise_for_status()
        data = resp.json()
        if self.verbose:
            print(f"  status: {resp.status_code}", file=sys.stderr)
        return data

    def _delete(self, path):
        url = f"{self.BASE_URL}{path}"
        if self.verbose:
            print(f"DELETE {url}", file=sys.stderr)
        resp = requests.delete(url, headers=self._headers())
        resp.raise_for_status()
        if resp.content:
            return resp.json()
        return {"status": resp.status_code}

    def get_doc(self):
        return self._get(f"/docs/{self.doc_id}")

    def list_tables(self):
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
        body = {"rows": [{"cells": cells}]}
        return self._post(f"/docs/{self.doc_id}/tables/{table_id}/rows", body)

    def upsert_rows(self, table_id, rows, key_columns):
        body = {"rows": rows, "keyColumns": key_columns}
        return self._post(f"/docs/{self.doc_id}/tables/{table_id}/rows", body)

    def delete_row(self, table_id, row_id):
        return self._delete(
            f"/docs/{self.doc_id}/tables/{table_id}/rows/{row_id}"
        )
