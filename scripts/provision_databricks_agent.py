"""Stores a simple Lactavia data-analyst agent in Microsoft Foundry, wired to the
Azure Databricks Genie MCP server so it can answer questions over
lactavia.supply_chain in Unity Catalog.

    python scripts/provision_databricks_agent.py

Configuration (environment or .env):
    AZURE_AI_PROJECT_ENDPOINT       Foundry project endpoint
    MODEL_DEPLOYMENT_NAME           model deployment backing the agent
    DATABRICKS_HOST                 adb-7405609622783779.19.azuredatabricks.net
    DATABRICKS_GENIE_SPACE_ID       required, the Genie Agent (space) id
    DATABRICKS_GENIE_CONNECTION_ID  optional project connection holding the
                                    Databricks OAuth credentials; create it once in
                                    Foundry under Tools > Azure Databricks Genie
"""

from __future__ import annotations

import os
import sys

from dotenv import load_dotenv

load_dotenv(override=False)

AGENT_NAME = "lactavia-data-analyst"

INSTRUCTIONS = """You are the Lactavia supply-chain data analyst.

Lactavia is a European dairy manufacturer. Its operational data lives in Unity Catalog
under lactavia.supply_chain: plants, products, suppliers and ingredient_inventory.

Answer questions by calling the Azure Databricks Genie tool with a clear, self-contained
natural-language question. Keep polling the tool until it returns a result; Genie can take
several seconds to plan and run the query.

Report the figures Genie returns, name the tables or columns they came from, and state the
units (kilograms, consumer units, euros, days). Never invent numbers: if Genie returns no
rows or an error, say so and suggest how to narrow the question. The tool is read-only, so
decline any request to modify data."""


def genie_endpoint(host: str, space_id: str) -> str:
    clean = host.removeprefix("https://").removeprefix("http://").rstrip("/")
    return f"https://{clean}/api/2.0/mcp/genie/{space_id}"


def main() -> int:
    endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT", "").rstrip("/")
    if not endpoint:
        print("AZURE_AI_PROJECT_ENDPOINT is not set.")
        return 1

    space_id = os.getenv("DATABRICKS_GENIE_SPACE_ID", "").strip()
    if not space_id:
        print(
            "DATABRICKS_GENIE_SPACE_ID is not set. Create a Genie Agent over "
            "lactavia.supply_chain in Databricks and copy its space id from the URL."
        )
        return 1

    host = os.getenv("DATABRICKS_HOST", "adb-7405609622783779.19.azuredatabricks.net")
    model = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4o")
    connection_id = os.getenv("DATABRICKS_GENIE_CONNECTION_ID", "").strip()
    server_url = genie_endpoint(host, space_id)

    from azure.ai.projects import AIProjectClient
    from azure.ai.projects.models import MCPTool, PromptAgentDefinition
    from azure.identity import DefaultAzureCredential

    tool = MCPTool(
        server_label="databricks_genie",
        server_url=server_url,
        server_description=(
            "Azure Databricks Genie over the Lactavia supply-chain tables: plants, "
            "products, suppliers and ingredient_inventory."
        ),
        require_approval="never",
        project_connection_id=connection_id or None,
    )

    with AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential()) as client:
        version = client.agents.create_version(
            agent_name=AGENT_NAME,
            definition=PromptAgentDefinition(
                model=model,
                instructions=INSTRUCTIONS,
                tools=[tool],
            ),
            description="Answers questions about Lactavia supply-chain data in Unity Catalog.",
            metadata={"app": "supply-disruption-response", "source": "databricks-genie"},
        )

    print(f"Project:    {endpoint}")
    print(f"Model:      {model}")
    print(f"Genie MCP:  {server_url}")
    print(f"Connection: {connection_id or 'none (finish the OAuth consent in the Foundry portal)'}")
    print(f"Stored:     {AGENT_NAME} version {version.version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
