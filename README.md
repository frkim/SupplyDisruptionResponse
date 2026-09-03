# Supply Disruption Response

An agentic solution demonstration: seventeen specialized AI agents detect, assess, and
coordinate the enterprise response to a critical ingredient supply disruption.

Built on Microsoft Foundry, Azure Container Apps, Cosmos DB, and Azure AI Search.

## The scenario

Lactovia is a European dairy group. Supplier `SUP-EU-014` in Valencia declares force majeure
on high-methoxyl pectin `ING-PEC-450`. Three plants deplete stock in twelve to eighteen days.
Fourteen SKUs across France, Germany, and Belgium are at risk.

No single agent can resolve this. The response requires situational awareness, three parallel
impact assessments, four remediation strategies, four specialist validations, a scored
comparison, an executive decision, and a coordinated execution plan.

## Orchestration

The workflow is a directed graph, not a chain. It demonstrates five orchestration patterns:

| Pattern | Where it appears |
|---------------------------|------------------------------------------------------------|
| Sequential spine | Signal to incident report to historical knowledge |
| Concurrent fan-out/fan-in | Three impact agents, then four specialist validators |
| Conditional routing | Deliberation runs only when the top two options are close |
| Human-in-the-loop | The executive gate suspends the run until a decision arrives |
| Graceful degradation | A failed agent is recorded and the graph continues |

```text
                    signal_normalizer
                           |
                     incident_report
                           |
                   historical_knowledge
                  /        |          \
        financial    operational    customer          <- concurrent
                  \        |          /
                     impact_synthesis
                           |
                    mitigation_planner
              /       |          |        \
      supply_chain  financial  regulatory  sustainability   <- concurrent
              \       |          |        /
                    scenario_evaluation
                           |
                      deliberation                    <- conditional
                           |
                     executive_gate                   <- human decision
                           |
                 stakeholder_coordination
                           |
                    executive_briefing
```

## Agent hosting modes

The solution deliberately runs agents three different ways, because real enterprises do:

* Foundry-hosted prompt agents invoked through the Foundry project.
* Local agents constructed in-process with Python function tools bound to live data.
* A2A agents called over HTTP through a JSON-RPC agent-card endpoint.

Every agent is grounded: fourteen function tools query Cosmos DB, and retrieval runs against
an Azure AI Search index built from a corporate knowledge corpus.

## Repository layout

| Path | Contents |
|-------------------|-------------------------------------------------------------------|
| `infra/` | Bicep: Foundry, Cosmos, Search, Storage, ACR, Container Apps, RBAC |
| `data/` | Thirteen seed datasets and eight knowledge documents |
| `src/backend/` | FastAPI application, agents, tools, orchestration engine |
| `src/frontend/` | React control-room UI with live DAG visualization |
| `scripts/` | Seeding and deployment automation |
| `.github/agents/` | Specialized agent definitions used to build the solution |

## Running it

Provision, seed, and deploy:

```powershell
az group create --name rg-supply-disruption --location swedencentral
az deployment group create --resource-group rg-supply-disruption --name sdr-core `
    --template-file infra/main.bicep --parameters infra/main.parameters.json

python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r src/backend/requirements.txt
.\.venv\Scripts\python.exe scripts/seed.py

pwsh ./scripts/deploy.ps1
```

Run locally against the provisioned Azure resources:

```powershell
cd src/backend
..\..\.venv\Scripts\python.exe -m uvicorn app.main:app --port 8000
```

Then start the UI with `npm run dev` in `src/frontend`.

## Authentication

Every Azure call uses `DefaultAzureCredential`. No keys or connection strings are read by the
application, and none are committed. The container app authenticates with a user-assigned
managed identity that holds only the roles it needs.

## Extension points

Two integrations are stubbed behind stable contracts so they can be added without refactoring:

* Databricks currently supplies the disruption signal through a bundled dataset. The signal
  contract is fixed, so a Databricks job can replace the stub directly.
* Copilot Studio can consume the orchestrator as a skill: every agent already publishes an
  A2A agent card, and the workflow exposes a streaming HTTP surface.
