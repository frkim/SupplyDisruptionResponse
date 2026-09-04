# Lactavia data in Databricks + a Foundry agent

Sample Unity Catalog data for Lactavia, plus a single Foundry agent that queries it through
the Azure Databricks Genie MCP server.

Workspace used by these files:

| Setting | Value |
| --- | --- |
| Server hostname | `adb-7405609622783779.19.azuredatabricks.net` |
| Workspace ID | `7405609622783779` |
| SQL warehouse | `ec3c62eb69ad9330` (`/sql/1.0/warehouses/ec3c62eb69ad9330`) |
| OAuth URL | `https://adb-7405609622783779.19.azuredatabricks.net/oidc` |

## 1. Seed the data

[lactavia_seed.sql](lactavia_seed.sql) creates `lactavia.supply_chain` with four tables:
`plants`, `products`, `suppliers`, `ingredient_inventory`. Every table and column carries a
comment, because that is what Genie reads when it decides which tables to query.

Run it either way:

- Paste the file into the Databricks SQL editor with warehouse `ec3c62eb69ad9330` selected.
- Or run `python scripts/seed_databricks.py`, which submits each statement through the SQL
  Statement Execution API. It authenticates with `DATABRICKS_TOKEN` when set, otherwise with
  `DefaultAzureCredential` (`az login`).

The script targets the existing `lactavia` catalog. This metastore uses Default Storage, so a
plain `CREATE CATALOG` fails — create new catalogs from the Databricks UI, or supply a
`MANAGED LOCATION`.

Seeded rows: 4 plants, 8 SKUs, 6 suppliers, 6 inventory records. Four plants hold
`ING-PEC-450`, with forecast stockouts between 2026-09-15 and 2026-09-21.

## 2. Create the Genie Agent

1. Enable the **Managed MCP Servers** preview: **Settings → Advanced → Previews**.
2. Create a Genie Agent scoped to the four `lactavia.supply_chain` tables, and give it a clear
   name and description.
3. Share it (`CAN RUN`) with the identity that will use the Foundry agent.
4. Copy the space id from the URL — that is `DATABRICKS_GENIE_SPACE_ID`.

This step has to happen in the UI: `POST /api/2.0/genie/spaces` requires an undocumented
`serialized_space` payload, so there is no supported scripted equivalent.

The space in use is `01f1a7a22ad81f16a0cd10d1c292eb4b` ("Supply Chain and Product Operations").

The MCP endpoint is then
`https://adb-7405609622783779.19.azuredatabricks.net/api/2.0/mcp/genie/<space-id>`.

## 3. Register a custom OAuth application

Genie MCP uses OAuth identity passthrough, so the Databricks account needs a custom OAuth app
(**Account console → Settings → App connections → Add connection**). Keep the client ID and
client secret; Foundry asks for both.

## 4. Connect the tool in Foundry

1. **Tools → Azure Databricks Genie → Connect**.
2. Remote MCP server endpoint: the URL from step 2.
3. Authentication: **OAuth identity passthrough**, with the client ID and secret from step 3.
4. Save, then copy the resulting project connection id into `DATABRICKS_GENIE_CONNECTION_ID`.

## 5. Store the agent

```powershell
$env:DATABRICKS_GENIE_SPACE_ID = '<space-id>'
$env:DATABRICKS_GENIE_CONNECTION_ID = '<connection-id>'
python scripts/provision_databricks_agent.py
```

This writes a `lactavia-data-analyst` agent version into the Foundry project with the Genie MCP
server attached. The first run prompts for consent: open it, sign in to Databricks, approve.

## Questions to try

- Which plants run out of high-methoxyl pectin first, and on what date?
- What weekly revenue is at risk across SKUs that use ING-PEC-450?
- Which qualified suppliers can cover ING-PEC-450, and what is their combined monthly capacity?
- Compare cost per kilogram and reliability for every ING-PEC-450 supplier.

## Limits

The Genie MCP server is read-only, carries no conversation history between turns, and enforces
Unity Catalog permissions on every request. For writes or deterministic SQL, use an OpenAPI or
Azure Function tool over the SQL Statement Execution API instead.
