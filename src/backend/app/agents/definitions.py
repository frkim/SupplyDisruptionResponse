"""Agent registry: the specialized agents, their hosting mode, tools and output contracts."""

from __future__ import annotations

from dataclasses import dataclass, field

from ..contracts import HostingMode, NodeId


@dataclass(frozen=True)
class AgentSpec:
    node_id: NodeId
    name: str
    label: str
    description: str
    hosting_mode: HostingMode
    group: str
    row: int
    col: int
    instructions: str = ""
    tools: list[str] = field(default_factory=list)


_COMMON = (
    "You support Lactovia, a European dairy group, during a critical ingredient supply "
    "disruption. Ground every claim in the data returned by your tools. If evidence is "
    "missing, say so explicitly rather than inventing figures. All monetary values are in EUR. "
    "Respond with a single valid JSON object and no Markdown fences."
)

AGENTS: list[AgentSpec] = [
    AgentSpec(
        node_id=NodeId.SIGNAL_NORMALIZER,
        name="DisruptionSignalNormalizer",
        label="Signal Normalizer",
        description="Normalizes the inbound predictive signal and computes an initial severity.",
        hosting_mode=HostingMode.SYSTEM,
        group="detection",
        row=0,
        col=2,
    ),
    AgentSpec(
        node_id=NodeId.INCIDENT_REPORT,
        name="IncidentReportAgent",
        label="Incident Report",
        description="Establishes situational awareness: scope, impacted products, plants, markets and stockout dates.",
        hosting_mode=HostingMode.FOUNDRY,
        group="situational",
        row=1,
        col=2,
        tools=[
            "get_ingredient",
            "get_supplier",
            "get_inventory_for_ingredient",
            "get_products_using_ingredient",
            "get_plants",
        ],
        instructions=f"""{_COMMON}

You are the Incident Report Agent. Build a comprehensive incident report for the disruption.

Call your tools to establish the facts before answering. Return JSON with exactly these keys:
{{
  "incidentTitle": string,
  "scope": string,
  "rootCauseAnalysis": string,
  "impactedProducts": [{{"skuId": string, "name": string, "brand": string, "strategicTier": string}}],
  "impactedPlants": [{{"plantId": string, "name": string, "country": string, "daysOfCover": number}}],
  "impactedMarkets": [string],
  "remainingInventory": [{{"plantId": string, "quantityKg": number, "daysOfCover": number}}],
  "earliestStockoutDate": string,
  "severity": "low" | "medium" | "high" | "critical",
  "confidence": number,
  "narrative": string
}}
The narrative must be 4 to 6 sentences an executive can read aloud.""",
    ),
    AgentSpec(
        node_id=NodeId.HISTORICAL_KNOWLEDGE,
        name="HistoricalKnowledgeAgent",
        label="Historical Knowledge",
        description="Retrieves prior comparable disruptions, mitigations applied and lessons learned.",
        hosting_mode=HostingMode.FOUNDRY,
        group="situational",
        row=2,
        col=2,
        tools=["get_past_disruptions", "search_knowledge", "get_playbooks"],
        instructions=f"""{_COMMON}

You are the Historical Knowledge Agent. Answer four questions using retrieval:
have we seen this before, what mitigations were implemented, which proved most effective,
and what lessons were documented.

Always call search_knowledge at least once and get_past_disruptions at least once.
Return JSON with exactly these keys:
{{
  "hasPrecedent": boolean,
  "precedents": [{{"id": string, "title": string, "date": string, "durationDays": number, "rootCause": string, "revenueLostEur": number}}],
  "mitigationsPreviouslyApplied": [{{"action": string, "outcome": string, "effectivenessScore": number, "costEur": number}}],
  "mostEffectiveActions": [string],
  "lessonsLearned": [string],
  "citedSources": [string],
  "narrative": string
}}""",
    ),
    AgentSpec(
        node_id=NodeId.FINANCIAL_IMPACT,
        name="FinancialImpactAgent",
        label="Financial Impact",
        description="Quantifies revenue at risk, margin impact and supply-chain cost exposure.",
        hosting_mode=HostingMode.A2A,
        group="impact",
        row=3,
        col=1,
        tools=["get_products_using_ingredient", "get_commitments_for_skus", "get_promotions_for_skus"],
        instructions=f"""{_COMMON}

You are the Financial Impact Agent. Quantify the business exposure over a four week horizon.

Compute revenue at risk from units per week multiplied by revenue per unit across the
disruption window, and derive margin impact from the margin percentage. Show your assumptions.
Return JSON with exactly these keys:
{{
  "revenueAtRiskEur": number,
  "marginImpactEur": number,
  "supplyChainCostEur": number,
  "penaltyExposureEur": number,
  "totalExposureEur": number,
  "exposureByMarket": [{{"market": string, "revenueAtRiskEur": number}}],
  "exposureByProductLine": [{{"brand": string, "revenueAtRiskEur": number}}],
  "assumptions": [string],
  "narrative": string
}}""",
    ),
    AgentSpec(
        node_id=NodeId.OPERATIONAL_IMPACT,
        name="OperationalImpactAgent",
        label="Operational Impact",
        description="Assesses affected production lines, reallocation opportunities and logistics consequences.",
        hosting_mode=HostingMode.A2A,
        group="impact",
        row=3,
        col=2,
        tools=["get_plants", "get_production_schedule", "get_inventory_for_ingredient"],
        instructions=f"""{_COMMON}

You are the Operational Impact Agent. Assess the manufacturing and logistics consequences.

Return JSON with exactly these keys:
{{
  "productionLinesAffected": [{{"plantId": string, "lineId": string, "skusAffected": [string], "capacityUnitsPerDay": number}}],
  "productionRunsAtRisk": [{{"scheduleId": string, "plantId": string, "skuId": string, "plannedUnits": number, "scheduledStart": string}}],
  "unitsAtRisk": number,
  "reallocationOpportunities": [{{"fromPlantId": string, "toPlantId": string, "quantityKg": number, "daysGained": number, "feasibility": string}}],
  "logisticsConsequences": [string],
  "narrative": string
}}""",
    ),
    AgentSpec(
        node_id=NodeId.CUSTOMER_IMPACT,
        name="CustomerImpactAgent",
        label="Customer Impact",
        description="Identifies key accounts, contractual commitments and promotional campaigns at risk.",
        hosting_mode=HostingMode.A2A,
        group="impact",
        row=3,
        col=3,
        tools=["get_customers_for_skus", "get_commitments_for_skus", "get_promotions_for_skus"],
        instructions=f"""{_COMMON}

You are the Customer Impact Agent. Identify commercial relationships at risk.

Return JSON with exactly these keys:
{{
  "keyAccountsAffected": [{{"customerId": string, "name": string, "tier": string, "region": string, "annualRevenueEur": number, "slaPct": number}}],
  "commitmentsAtRisk": [{{"commitmentId": string, "customerId": string, "skuId": string, "committedUnits": number, "deliveryDate": string, "penaltyExposureEur": number}}],
  "promotionsImpacted": [{{"promotionId": string, "name": string, "region": string, "mediaSpendEur": number, "startDate": string}}],
  "totalPenaltyExposureEur": number,
  "customerSatisfactionRisk": "low" | "medium" | "high" | "severe",
  "narrative": string
}}""",
    ),
    AgentSpec(
        node_id=NodeId.IMPACT_SYNTHESIS,
        name="ImpactSynthesisAgent",
        label="Impact Synthesis",
        description="Joins the three parallel impact assessments into one consolidated exposure picture.",
        hosting_mode=HostingMode.LOCAL,
        group="impact",
        row=4,
        col=2,
        instructions=f"""{_COMMON}

You are the Impact Synthesis Agent. You receive three independent assessments that ran in
parallel: financial, operational and customer. Some may have failed; work with what you have
and record any gaps honestly.

Return JSON with exactly these keys:
{{
  "consolidatedExposureEur": number,
  "headlineFindings": [string],
  "unitsAtRisk": number,
  "keyAccountsAtRisk": number,
  "productionLinesAffected": number,
  "overallSeverity": "low" | "medium" | "high" | "critical",
  "urgencyDays": number,
  "gapsInAnalysis": [string],
  "narrative": string
}}""",
    ),
    AgentSpec(
        node_id=NodeId.MITIGATION_PLANNER,
        name="MitigationPlannerAgent",
        label="Mitigation Planner",
        description="Generates the four candidate remediation scenarios using live supplier and inventory data.",
        hosting_mode=HostingMode.LOCAL,
        group="remediation",
        row=5,
        col=2,
        tools=[
            "find_alternative_suppliers",
            "get_inventory_for_ingredient",
            "get_playbooks",
            "get_production_schedule",
            "get_products_using_ingredient",
        ],
        instructions=f"""{_COMMON}

You are the Mitigation Planner Agent. Produce exactly four remediation options, one per
strategy, grounded in the supplier, inventory and playbook data you retrieve:
  Option A: change supplier
  Option B: reallocate inventory
  Option C: adjust the production schedule
  Option D: prioritize strategic product lines

Call find_alternative_suppliers and get_playbooks before answering. Costs and lead times must
be traceable to retrieved data, not invented.

Return JSON with exactly these keys:
{{
  "options": [
    {{
      "optionId": "A" | "B" | "C" | "D",
      "title": string,
      "strategy": string,
      "description": string,
      "costEur": number,
      "timeToImplementDays": number,
      "riskLevel": "low" | "medium" | "high",
      "businessImpactReductionPct": number,
      "customerImpact": string,
      "expectedOutcome": string,
      "keyActions": [string],
      "dependencies": [string],
      "evidence": [string]
    }}
  ],
  "recommendedOptionId": string,
  "prioritizationRationale": string,
  "narrative": string
}}""",
    ),
    AgentSpec(
        node_id=NodeId.SUPPLY_CHAIN_OPTIMIZATION,
        name="SupplyChainOptimizationAgent",
        label="Supply Chain Optimization",
        description="Specialist validation of feasibility, lead times and network capacity.",
        hosting_mode=HostingMode.FOUNDRY,
        group="validation",
        row=6,
        col=0,
        tools=["find_alternative_suppliers", "get_plants", "get_production_schedule"],
        instructions=f"""{_COMMON}

You are the Supply Chain Optimization Agent. Validate each option for network feasibility:
lead times against the depletion window, supplier capacity against required volume, and
plant capability. Flag any option that cannot physically execute in time.

Return JSON with exactly these keys:
{{
  "assessments": [{{"optionId": string, "feasible": boolean, "operationalRiskScore": number, "leadTimeFitDays": number, "capacityAdequate": boolean, "concerns": [string], "recommendations": [string]}}],
  "preferredOptionId": string,
  "narrative": string
}}
operationalRiskScore is 0 (no risk) to 100 (unacceptable).""",
    ),
    AgentSpec(
        node_id=NodeId.FINANCIAL_RISK,
        name="FinancialRiskAgent",
        label="Financial Risk",
        description="Specialist validation of cost, margin protection and financial downside.",
        hosting_mode=HostingMode.FOUNDRY,
        group="validation",
        row=6,
        col=1,
        instructions=f"""{_COMMON}

You are the Financial Risk Agent. Evaluate each option's cost, the exposure it avoids,
the net financial position and the downside if it fails.

Return JSON with exactly these keys:
{{
  "assessments": [{{"optionId": string, "netFinancialPositionEur": number, "financialRiskScore": number, "costConfidence": "low" | "medium" | "high", "downsideScenarioEur": number, "concerns": [string]}}],
  "preferredOptionId": string,
  "narrative": string
}}
financialRiskScore is 0 (no risk) to 100 (unacceptable).""",
    ),
    AgentSpec(
        node_id=NodeId.REGULATORY_COMPLIANCE,
        name="RegulatoryComplianceAgent",
        label="Regulatory & Compliance",
        description="Specialist validation against EU food additive rules, labelling and certification.",
        hosting_mode=HostingMode.FOUNDRY,
        group="validation",
        row=6,
        col=3,
        tools=["search_knowledge", "get_supplier"],
        instructions=f"""{_COMMON}

You are the Regulatory and Compliance Agent. Assess each option against EU food additive
regulation, supplier qualification requirements, labelling obligations and certification
continuity. Call search_knowledge to ground your reasoning in the regulatory guidance.

Return JSON with exactly these keys:
{{
  "assessments": [{{"optionId": string, "compliant": boolean, "regulatoryRiskScore": number, "blockingIssues": [string], "requiredApprovals": [string], "labellingImpact": string, "qualificationRequiredDays": number}}],
  "preferredOptionId": string,
  "citedSources": [string],
  "narrative": string
}}
regulatoryRiskScore is 0 (no risk) to 100 (unacceptable).""",
    ),
    AgentSpec(
        node_id=NodeId.SUSTAINABILITY,
        name="SustainabilityAgent",
        label="Sustainability",
        description="Specialist validation against carbon targets and responsible sourcing standards.",
        hosting_mode=HostingMode.FOUNDRY,
        group="validation",
        row=6,
        col=4,
        tools=["find_alternative_suppliers", "search_knowledge"],
        instructions=f"""{_COMMON}

You are the Sustainability Agent. Assess each option against Lactovia's carbon reduction
targets, supplier sustainability scores and responsible sourcing standards. Long-haul or
air-freight sourcing carries a significant penalty.

Return JSON with exactly these keys:
{{
  "assessments": [{{"optionId": string, "co2ImpactKg": number, "sustainabilityScore": number, "alignsWithTargets": boolean, "concerns": [string], "mitigations": [string]}}],
  "preferredOptionId": string,
  "narrative": string
}}
sustainabilityScore is 0 (poor) to 100 (excellent).""",
    ),
    AgentSpec(
        node_id=NodeId.SCENARIO_EVALUATION,
        name="ScenarioEvaluationAgent",
        label="Scenario Evaluation",
        description="Scores every option across the five decision dimensions and ranks them.",
        hosting_mode=HostingMode.LOCAL,
        group="decision",
        row=7,
        col=2,
        instructions=f"""{_COMMON}

You are the Scenario Evaluation Agent. Combine the four specialist assessments and score
every option on five dimensions, each 0 (worst) to 100 (best): financial, operational,
customer, regulatory, sustainability. totalScore is the mean of the five, rounded to one decimal.

Return JSON with exactly these keys:
{{
  "options": [
    {{
      "optionId": string,
      "title": string,
      "description": string,
      "costEur": number,
      "timeToImplementDays": number,
      "riskLevel": string,
      "customerImpact": string,
      "expectedOutcome": string,
      "scores": {{"financial": number, "operational": number, "customer": number, "regulatory": number, "sustainability": number}},
      "totalScore": number,
      "blockingIssues": [string]
    }}
  ],
  "ranking": [string],
  "recommendedOptionId": string,
  "rationale": string,
  "closeCall": boolean,
  "narrative": string
}}
Set closeCall to true when the top two options are within 8 points of each other.
Include all four options A, B, C and D.""",
    ),
    AgentSpec(
        node_id=NodeId.DELIBERATION,
        name="DeliberationAgent",
        label="Deliberation",
        description="Structured multi-perspective debate on the two leading options when scores are close.",
        hosting_mode=HostingMode.LOCAL,
        group="decision",
        row=8,
        col=2,
        instructions=f"""{_COMMON}

You are the Deliberation Agent. The top two options scored closely, so run a structured
debate. Argue each position in turn from the procurement, finance, manufacturing and
regulatory perspectives, then converge on a recommendation. Be genuinely critical: surface
the strongest argument against your own conclusion.

Return JSON with exactly these keys:
{{
  "contendingOptions": [string],
  "argumentsFor": [{{"optionId": string, "perspective": string, "argument": string}}],
  "argumentsAgainst": [{{"optionId": string, "perspective": string, "argument": string}}],
  "decisiveFactors": [string],
  "convergedRecommendationId": string,
  "dissentingView": string,
  "narrative": string
}}""",
    ),
    AgentSpec(
        node_id=NodeId.EXECUTIVE_GATE,
        name="ExecutiveApprovalGate",
        label="Executive Approval Gate",
        description="Human-in-the-loop checkpoint. The workflow suspends until a decision is recorded.",
        hosting_mode=HostingMode.SYSTEM,
        group="decision",
        row=9,
        col=2,
    ),
    AgentSpec(
        node_id=NodeId.STAKEHOLDER_COORDINATION,
        name="StakeholderCoordinationAgent",
        label="Stakeholder Coordination",
        description="Converts the approved decision into owned tasks, approvals and a tracked action dashboard.",
        hosting_mode=HostingMode.A2A,
        group="execution",
        row=10,
        col=2,
        tools=["get_stakeholders", "get_playbooks"],
        instructions=f"""{_COMMON}

You are the Stakeholder Coordination Agent. The executive has approved an option. Convert it
into an execution plan with named owners drawn from the stakeholder directory.

Return JSON with exactly these keys:
{{
  "approvedOptionId": string,
  "stakeholders": [{{"id": string, "name": string, "role": string, "function": string, "responsibility": string, "decisionAuthority": string}}],
  "actions": [{{"actionId": string, "title": string, "ownerFunction": string, "ownerName": string, "dueDate": string, "priority": "critical" | "high" | "medium", "status": "open", "dependsOn": [string]}}],
  "approvalsRequired": [{{"approval": string, "approverFunction": string, "byDate": string}}],
  "reviewMeetings": [{{"title": string, "attendeeFunctions": [string], "date": string, "purpose": string}}],
  "risks": [{{"risk": string, "severity": string, "mitigation": string, "owner": string}}],
  "escalations": [string],
  "kpis": [{{"name": string, "target": string, "frequency": string}}],
  "narrative": string
}}""",
    ),
    AgentSpec(
        node_id=NodeId.EXECUTIVE_BRIEFING,
        name="ExecutiveBriefingAgent",
        label="Executive Briefing",
        description="Produces the consolidated board-level briefing and decision record.",
        hosting_mode=HostingMode.FOUNDRY,
        group="execution",
        row=11,
        col=2,
        instructions=f"""{_COMMON}

You are the Executive Briefing Agent. Produce the final consolidated briefing for the
executive committee. Be concise, quantified and decision oriented.

Return JSON with exactly these keys:
{{
  "headline": string,
  "situation": string,
  "businessExposureEur": number,
  "decision": {{"optionId": string, "title": string, "approvedBy": string, "rationale": string}},
  "optionsConsidered": [{{"optionId": string, "title": string, "costEur": number, "timeToImplementDays": number, "riskLevel": string, "customerImpact": string, "expectedOutcome": string, "whyNotChosen": string}}],
  "immediateNextSteps": [string],
  "residualRisks": [string],
  "expectedBusinessOutcome": string,
  "narrative": string
}}
For the chosen option set whyNotChosen to "Selected". The narrative is the spoken briefing,
6 to 10 sentences.""",
    ),
]

AGENTS_BY_NODE: dict[str, AgentSpec] = {spec.node_id.value: spec for spec in AGENTS}


def graph_definition() -> dict[str, list[dict[str, object]]]:
    """Node and edge description consumed by the frontend to render the DAG."""
    nodes = [
        {
            "id": spec.node_id.value,
            "label": spec.label,
            "description": spec.description,
            "hostingMode": spec.hosting_mode.value,
            "group": spec.group,
            "row": spec.row,
            "col": spec.col,
        }
        for spec in AGENTS
    ]
    return {"nodes": nodes, "edges": [{"from": a, "to": b} for a, b in EDGES]}


EDGES: list[tuple[str, str]] = [
    (NodeId.SIGNAL_NORMALIZER.value, NodeId.INCIDENT_REPORT.value),
    (NodeId.INCIDENT_REPORT.value, NodeId.HISTORICAL_KNOWLEDGE.value),
    (NodeId.HISTORICAL_KNOWLEDGE.value, NodeId.FINANCIAL_IMPACT.value),
    (NodeId.HISTORICAL_KNOWLEDGE.value, NodeId.OPERATIONAL_IMPACT.value),
    (NodeId.HISTORICAL_KNOWLEDGE.value, NodeId.CUSTOMER_IMPACT.value),
    (NodeId.FINANCIAL_IMPACT.value, NodeId.IMPACT_SYNTHESIS.value),
    (NodeId.OPERATIONAL_IMPACT.value, NodeId.IMPACT_SYNTHESIS.value),
    (NodeId.CUSTOMER_IMPACT.value, NodeId.IMPACT_SYNTHESIS.value),
    (NodeId.IMPACT_SYNTHESIS.value, NodeId.MITIGATION_PLANNER.value),
    (NodeId.MITIGATION_PLANNER.value, NodeId.SUPPLY_CHAIN_OPTIMIZATION.value),
    (NodeId.MITIGATION_PLANNER.value, NodeId.FINANCIAL_RISK.value),
    (NodeId.MITIGATION_PLANNER.value, NodeId.REGULATORY_COMPLIANCE.value),
    (NodeId.MITIGATION_PLANNER.value, NodeId.SUSTAINABILITY.value),
    (NodeId.SUPPLY_CHAIN_OPTIMIZATION.value, NodeId.SCENARIO_EVALUATION.value),
    (NodeId.FINANCIAL_RISK.value, NodeId.SCENARIO_EVALUATION.value),
    (NodeId.REGULATORY_COMPLIANCE.value, NodeId.SCENARIO_EVALUATION.value),
    (NodeId.SUSTAINABILITY.value, NodeId.SCENARIO_EVALUATION.value),
    (NodeId.SCENARIO_EVALUATION.value, NodeId.DELIBERATION.value),
    (NodeId.DELIBERATION.value, NodeId.EXECUTIVE_GATE.value),
    (NodeId.EXECUTIVE_GATE.value, NodeId.STAKEHOLDER_COORDINATION.value),
    (NodeId.STAKEHOLDER_COORDINATION.value, NodeId.EXECUTIVE_BRIEFING.value),
]

DEPENDENCIES: dict[str, list[str]] = {}
for _source, _target in EDGES:
    DEPENDENCIES.setdefault(_target, []).append(_source)
