"""Loads databricks/lactavia_seed.sql into Unity Catalog through the Databricks
SQL Statement Execution API.

    python scripts/seed_databricks.py

Configuration (environment or .env):
    DATABRICKS_HOST          adb-7405609622783779.19.azuredatabricks.net
    DATABRICKS_HTTP_PATH     /sql/1.0/warehouses/ec3c62eb69ad9330
    DATABRICKS_TOKEN         optional PAT; omitted means Entra ID via DefaultAzureCredential
"""

from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv(override=False)

ROOT = Path(__file__).resolve().parents[1]
SEED_FILE = ROOT / "databricks" / "lactavia_seed.sql"

# Fixed Entra ID application ID of the Azure Databricks service.
DATABRICKS_SCOPE = "2ff814a6-3304-4ab8-85cb-cd0e6f879c1d/.default"

HOST = os.getenv("DATABRICKS_HOST", "adb-7405609622783779.19.azuredatabricks.net").strip()
HTTP_PATH = os.getenv("DATABRICKS_HTTP_PATH", "/sql/1.0/warehouses/ec3c62eb69ad9330").strip()
POLL_SECONDS = 2.0
POLL_ATTEMPTS = 90


def base_url() -> str:
    host = HOST.removeprefix("https://").removeprefix("http://").rstrip("/")
    return f"https://{host}"


def warehouse_id() -> str:
    return HTTP_PATH.rstrip("/").rsplit("/", 1)[-1]


def bearer_token() -> str:
    token = os.getenv("DATABRICKS_TOKEN", "").strip()
    if token:
        return token

    from azure.identity import DefaultAzureCredential

    return DefaultAzureCredential().get_token(DATABRICKS_SCOPE).token


def statements(sql: str) -> list[str]:
    """Split the seed file on semicolons, ignoring comment-only fragments."""
    chunks = []
    for raw in sql.split(";"):
        body = re.sub(r"--[^\n]*", "", raw).strip()
        if body:
            chunks.append(raw.strip())
    return chunks


def execute(client: httpx.Client, statement: str) -> None:
    response = client.post(
        "/api/2.0/sql/statements",
        json={
            "statement": statement,
            "warehouse_id": warehouse_id(),
            "wait_timeout": "30s",
            "on_wait_timeout": "CONTINUE",
        },
    )
    response.raise_for_status()
    payload = response.json()

    for _ in range(POLL_ATTEMPTS):
        state = payload.get("status", {}).get("state", "")
        if state == "SUCCEEDED":
            return
        if state in {"FAILED", "CANCELED", "CLOSED"}:
            error = payload.get("status", {}).get("error", {}).get("message", state)
            raise RuntimeError(error)
        time.sleep(POLL_SECONDS)
        poll = client.get(f"/api/2.0/sql/statements/{payload['statement_id']}")
        poll.raise_for_status()
        payload = poll.json()

    raise RuntimeError("Statement did not complete within the polling window.")


def main() -> int:
    if not SEED_FILE.exists():
        print(f"Seed file not found: {SEED_FILE}")
        return 1

    batch = statements(SEED_FILE.read_text(encoding="utf-8"))
    print(f"Warehouse: {warehouse_id()} on {base_url()}")
    print(f"Statements: {len(batch)}\n")

    with httpx.Client(
        base_url=base_url(),
        headers={"Authorization": f"Bearer {bearer_token()}"},
        timeout=120.0,
    ) as client:
        for index, statement in enumerate(batch, start=1):
            label = " ".join(statement.split())[:72]
            try:
                execute(client, statement)
                print(f"  [{index:>2}/{len(batch)}] ok   {label}")
            except Exception as exc:
                print(f"  [{index:>2}/{len(batch)}] FAIL {label}\n         {exc}")
                return 2

    print("\nSeeded lactavia.supply_chain (plants, products, suppliers, ingredient_inventory).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
