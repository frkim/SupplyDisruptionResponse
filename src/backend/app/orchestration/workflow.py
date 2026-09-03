"""The Supply Disruption Response workflow.

Builds prompts from the run context, wires the agent graph, and implements the
human-in-the-loop executive gate.
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from ..agents.definitions import AGENTS_BY_NODE, DEPENDENCIES
from ..agents.runner import run_agent
from ..config import get_settings
from ..contracts import (
    DisruptionSignal,
    EventType,
    HostingMode,
    NodeId,
    NodeResult,
    NodeState,
    RunContext,
)
from .engine import REGISTRY, Node, Orchestrator

logger = logging.getLogger(__name__)


def _compact(payload: Any, limit: int = 6000) -> str:
    text = json.dumps(payload, default=str, ensure_ascii=False)
    return text[:limit]


def _signal_block(ctx: RunContext) -> str:
    signal = ctx.signal.to_dict() if ctx.signal else {}
    return f"DISRUPTION SIGNAL:\n{_compact(signal)}"


def _severity(ctx: RunContext) -> str:
    report = ctx.structured_of(NodeId.INCIDENT_REPORT)
    synthesis = ctx.structured_of(NodeId.IMPACT_SYNTHESIS)
    return str(
        synthesis.get("overallSeverity") or report.get("severity") or "high"
    ).lower()


# --------------------------------------------------------------------------------------
# Prompt builders
# --------------------------------------------------------------------------------------

def _prompt_incident_report(ctx: RunContext) -> str:
    return (
        f"{_signal_block(ctx)}\n\n"
        "Investigate this disruption. Retrieve the ingredient, its supplier, inventory at "
        "every plant, and the finished-goods SKUs that depend on it. Then produce the "
        "incident report JSON."
    )


def _prompt_historical(ctx: RunContext) -> str:
    report = ctx.structured_of(NodeId.INCIDENT_REPORT)
    ingredient = ctx.signal.ingredient_id if ctx.signal else ""
    return (
        f"{_signal_block(ctx)}\n\n"
        f"INCIDENT REPORT:\n{_compact(report, 3500)}\n\n"
        f"Search the knowledge corpus for prior disruptions involving {ingredient}, pectin "
        "shortages, and the mitigation playbooks that were used. Produce the historical "
        "knowledge JSON."
    )


def _impact_preamble(ctx: RunContext) -> str:
    report = ctx.structured_of(NodeId.INCIDENT_REPORT)
    history = ctx.structured_of(NodeId.HISTORICAL_KNOWLEDGE)
    return (
        f"{_signal_block(ctx)}\n\n"
        f"INCIDENT REPORT:\n{_compact(report, 3000)}\n\n"
        f"HISTORICAL CONTEXT:\n{_compact(history, 2000)}"
    )


def _prompt_financial_impact(ctx: RunContext) -> str:
    skus = ctx.signal.impacted_skus if ctx.signal else []
    return (
        f"{_impact_preamble(ctx)}\n\n"
        f"Impacted SKUs: {skus}\n"
        "Quantify the financial exposure. Produce the financial impact JSON."
    )


def _prompt_operational_impact(ctx: RunContext) -> str:
    plants = ctx.signal.affected_plants if ctx.signal else []
    return (
        f"{_impact_preamble(ctx)}\n\n"
        f"Affected plants: {plants}\n"
        "Assess production and logistics consequences. Produce the operational impact JSON."
    )


def _prompt_customer_impact(ctx: RunContext) -> str:
    skus = ctx.signal.impacted_skus if ctx.signal else []
    return (
        f"{_impact_preamble(ctx)}\n\n"
        f"Impacted SKUs: {skus}\n"
        "Identify accounts, commitments and promotions at risk. Produce the customer impact JSON."
    )


def _prompt_synthesis(ctx: RunContext) -> str:
    parts = []
    for node_id, label in (
        (NodeId.FINANCIAL_IMPACT, "FINANCIAL IMPACT"),
        (NodeId.OPERATIONAL_IMPACT, "OPERATIONAL IMPACT"),
        (NodeId.CUSTOMER_IMPACT, "CUSTOMER IMPACT"),
    ):
        result = ctx.get(node_id)
        if result and result.state is NodeState.COMPLETED:
            parts.append(f"{label}:\n{_compact(result.structured, 3000)}")
        else:
            parts.append(f"{label}: NOT AVAILABLE (the assessment did not complete)")
    return (
        f"{_signal_block(ctx)}\n\n" + "\n\n".join(parts) + "\n\n"
        "Consolidate these parallel assessments. Produce the synthesis JSON."
    )


def _prompt_mitigation(ctx: RunContext) -> str:
    synthesis = ctx.structured_of(NodeId.IMPACT_SYNTHESIS)
    history = ctx.structured_of(NodeId.HISTORICAL_KNOWLEDGE)
    ingredient = ctx.signal.ingredient_id if ctx.signal else ""
    return (
        f"{_signal_block(ctx)}\n\n"
        f"CONSOLIDATED IMPACT:\n{_compact(synthesis, 3000)}\n\n"
        f"WHAT WORKED PREVIOUSLY:\n{_compact(history.get('mostEffectiveActions', []), 1500)}\n\n"
        f"Find alternative suppliers for {ingredient} and the relevant playbooks, then produce "
        "the four remediation options as JSON."
    )


def _specialist_prompt(ctx: RunContext, focus: str) -> str:
    options = ctx.structured_of(NodeId.MITIGATION_PLANNER).get("options", [])
    synthesis = ctx.structured_of(NodeId.IMPACT_SYNTHESIS)
    return (
        f"{_signal_block(ctx)}\n\n"
        f"CONSOLIDATED IMPACT:\n{_compact(synthesis, 2000)}\n\n"
        f"CANDIDATE OPTIONS:\n{_compact(options, 6000)}\n\n"
        f"{focus} Assess every option (A, B, C and D) and produce your JSON."
    )


def _prompt_evaluation(ctx: RunContext) -> str:
    options = ctx.structured_of(NodeId.MITIGATION_PLANNER).get("options", [])
    blocks = [f"CANDIDATE OPTIONS:\n{_compact(options, 5000)}"]
    for node_id, label in (
        (NodeId.SUPPLY_CHAIN_OPTIMIZATION, "SUPPLY CHAIN OPTIMIZATION"),
        (NodeId.FINANCIAL_RISK, "FINANCIAL RISK"),
        (NodeId.REGULATORY_COMPLIANCE, "REGULATORY AND COMPLIANCE"),
        (NodeId.SUSTAINABILITY, "SUSTAINABILITY"),
    ):
        result = ctx.get(node_id)
        if result and result.state is NodeState.COMPLETED:
            blocks.append(f"{label} ASSESSMENT:\n{_compact(result.structured, 2500)}")
        else:
            blocks.append(f"{label} ASSESSMENT: NOT AVAILABLE")
    return "\n\n".join(blocks) + "\n\nScore and rank the options. Produce the evaluation JSON."


def _prompt_deliberation(ctx: RunContext) -> str:
    evaluation = ctx.structured_of(NodeId.SCENARIO_EVALUATION)
    return (
        f"EVALUATION RESULT:\n{_compact(evaluation, 6000)}\n\n"
        "The leading options are close. Debate them and converge. Produce the deliberation JSON."
    )


def _prompt_stakeholder(ctx: RunContext) -> str:
    decision = ctx.decision or {}
    evaluation = ctx.structured_of(NodeId.SCENARIO_EVALUATION)
    chosen = decision.get("optionId", "")
    return (
        f"APPROVED OPTION: {chosen}\n"
        f"APPROVER: {decision.get('approver', 'Executive Committee')}\n"
        f"APPROVAL NOTES: {decision.get('notes', '(none)')}\n\n"
        f"EVALUATION:\n{_compact(evaluation, 4000)}\n\n"
        "Retrieve the stakeholder directory and the relevant playbook, then produce the "
        "coordination JSON with named owners."
    )


def _prompt_briefing(ctx: RunContext) -> str:
    return (
        f"{_signal_block(ctx)}\n\n"
        f"CONSOLIDATED IMPACT:\n{_compact(ctx.structured_of(NodeId.IMPACT_SYNTHESIS), 2500)}\n\n"
        f"EVALUATION:\n{_compact(ctx.structured_of(NodeId.SCENARIO_EVALUATION), 4000)}\n\n"
        f"DECISION:\n{_compact(ctx.decision or {}, 1000)}\n\n"
        f"EXECUTION PLAN:\n{_compact(ctx.structured_of(NodeId.STAKEHOLDER_COORDINATION), 2500)}\n\n"
        "Produce the executive briefing JSON."
    )


_PROMPTS = {
    NodeId.INCIDENT_REPORT: _prompt_incident_report,
    NodeId.HISTORICAL_KNOWLEDGE: _prompt_historical,
    NodeId.FINANCIAL_IMPACT: _prompt_financial_impact,
    NodeId.OPERATIONAL_IMPACT: _prompt_operational_impact,
    NodeId.CUSTOMER_IMPACT: _prompt_customer_impact,
    NodeId.IMPACT_SYNTHESIS: _prompt_synthesis,
    NodeId.MITIGATION_PLANNER: _prompt_mitigation,
    NodeId.SUPPLY_CHAIN_OPTIMIZATION: lambda c: _specialist_prompt(
        c, "You are validating network feasibility, lead times and capacity."
    ),
    NodeId.FINANCIAL_RISK: lambda c: _specialist_prompt(
        c, "You are validating cost, margin protection and financial downside."
    ),
    NodeId.REGULATORY_COMPLIANCE: lambda c: _specialist_prompt(
        c, "You are validating regulatory, labelling and qualification constraints."
    ),
    NodeId.SUSTAINABILITY: lambda c: _specialist_prompt(
        c, "You are validating carbon impact and responsible sourcing alignment."
    ),
    NodeId.SCENARIO_EVALUATION: _prompt_evaluation,
    NodeId.DELIBERATION: _prompt_deliberation,
    NodeId.STAKEHOLDER_COORDINATION: _prompt_stakeholder,
    NodeId.EXECUTIVE_BRIEFING: _prompt_briefing,
}


# --------------------------------------------------------------------------------------
# Node executors
# --------------------------------------------------------------------------------------

def _agent_executor(node_id: NodeId):
    async def execute(ctx: RunContext) -> NodeResult:
        spec = AGENTS_BY_NODE[node_id.value]
        prompt = _PROMPTS[node_id](ctx)
        return await run_agent(spec, prompt)

    return execute


async def _normalize_signal(ctx: RunContext) -> NodeResult:
    """Deterministic pre-processing. Stands in for the Databricks detection job."""
    spec = AGENTS_BY_NODE[NodeId.SIGNAL_NORMALIZER.value]
    signal = ctx.signal
    result = NodeResult(
        node_id=spec.node_id.value,
        agent_name=spec.name,
        hosting_mode=HostingMode.SYSTEM,
        state=NodeState.COMPLETED,
    )
    if signal is None:
        result.state = NodeState.FAILED
        result.error = "no signal supplied"
        return result

    urgency = signal.depletion_days_min
    if urgency <= 7:
        severity = "critical"
    elif urgency <= 14:
        severity = "high"
    elif urgency <= 30:
        severity = "medium"
    else:
        severity = "low"

    result.structured = {
        "incidentId": ctx.incident_id,
        "ingredientId": signal.ingredient_id,
        "ingredientName": signal.ingredient_name,
        "supplierId": signal.supplier_id,
        "confidence": signal.confidence,
        "depletionWindowDays": [signal.depletion_days_min, signal.depletion_days_max],
        "impactedSkuCount": len(signal.impacted_skus),
        "affectedRegions": signal.affected_regions,
        "affectedPlants": signal.affected_plants,
        "initialSeverity": severity,
        "source": signal.source,
    }
    result.narrative = (
        f"Signal accepted from {signal.source} at confidence {signal.confidence:.2f}. "
        f"{signal.ingredient_name} ({signal.ingredient_id}) from supplier {signal.supplier_id} "
        f"depletes in {signal.depletion_days_min} to {signal.depletion_days_max} days across "
        f"{len(signal.affected_plants)} plants, placing {len(signal.impacted_skus)} SKUs at risk "
        f"in {', '.join(signal.affected_regions)}. Initial severity classified as {severity}."
    )
    return result


def _make_gate_handler():
    async def handle(ctx: RunContext, emit) -> NodeResult:
        settings = get_settings()
        spec = AGENTS_BY_NODE[NodeId.EXECUTIVE_GATE.value]
        evaluation = ctx.structured_of(NodeId.SCENARIO_EVALUATION)
        deliberation = ctx.structured_of(NodeId.DELIBERATION)

        options = evaluation.get("options", [])
        recommended = (
            deliberation.get("convergedRecommendationId")
            or evaluation.get("recommendedOptionId")
            or (options[0].get("optionId") if options else "A")
        )
        rationale = (
            deliberation.get("narrative")
            or evaluation.get("rationale")
            or "Highest weighted score across the five decision dimensions."
        )

        loop = asyncio.get_running_loop()
        future: asyncio.Future = loop.create_future()
        REGISTRY.set_gate(ctx.run_id, future)

        await emit(
            {
                "type": EventType.GATE_AWAITING.value,
                "nodeId": spec.node_id.value,
                "runId": ctx.run_id,
                "options": options,
                "recommendation": {"optionId": recommended, "rationale": rationale},
            }
        )

        result = NodeResult(
            node_id=spec.node_id.value,
            agent_name=spec.name,
            hosting_mode=HostingMode.SYSTEM,
        )

        try:
            decision = await asyncio.wait_for(future, timeout=settings.gate_timeout)
        except asyncio.TimeoutError:
            decision = {
                "optionId": recommended,
                "approver": "Auto-approved (gate timeout)",
                "notes": "No human decision was recorded before the gate expired.",
                "autoApproved": True,
            }

        ctx.decision = decision
        result.state = NodeState.COMPLETED
        result.structured = {
            "approvedOptionId": decision.get("optionId"),
            "approver": decision.get("approver"),
            "notes": decision.get("notes"),
            "autoApproved": decision.get("autoApproved", False),
            "recommendationFollowed": decision.get("optionId") == recommended,
        }
        result.narrative = (
            f"Option {decision.get('optionId')} approved by {decision.get('approver')}. "
            f"{'This matches' if decision.get('optionId') == recommended else 'This overrides'} "
            f"the system recommendation of option {recommended}."
        )
        return result

    return handle


def build_orchestrator() -> Orchestrator:
    settings = get_settings()

    def deliberation_condition(ctx: RunContext) -> bool:
        if not settings.enable_deliberation:
            return False
        evaluation = ctx.structured_of(NodeId.SCENARIO_EVALUATION)
        if evaluation.get("closeCall") is True:
            return True
        scores = sorted(
            (float(o.get("totalScore", 0) or 0) for o in evaluation.get("options", [])),
            reverse=True,
        )
        return len(scores) >= 2 and (scores[0] - scores[1]) <= 8.0

    nodes = [Node(NodeId.SIGNAL_NORMALIZER.value, _normalize_signal, depends_on=[])]

    for node_id in (
        NodeId.INCIDENT_REPORT,
        NodeId.HISTORICAL_KNOWLEDGE,
        NodeId.FINANCIAL_IMPACT,
        NodeId.OPERATIONAL_IMPACT,
        NodeId.CUSTOMER_IMPACT,
        NodeId.IMPACT_SYNTHESIS,
        NodeId.MITIGATION_PLANNER,
        NodeId.SUPPLY_CHAIN_OPTIMIZATION,
        NodeId.FINANCIAL_RISK,
        NodeId.REGULATORY_COMPLIANCE,
        NodeId.SUSTAINABILITY,
        NodeId.SCENARIO_EVALUATION,
    ):
        nodes.append(
            Node(
                node_id.value,
                _agent_executor(node_id),
                depends_on=DEPENDENCIES.get(node_id.value, []),
            )
        )

    nodes.append(
        Node(
            NodeId.DELIBERATION.value,
            _agent_executor(NodeId.DELIBERATION),
            depends_on=DEPENDENCIES.get(NodeId.DELIBERATION.value, []),
            condition=deliberation_condition,
        )
    )
    nodes.append(
        Node(
            NodeId.EXECUTIVE_GATE.value,
            _normalize_signal,  # replaced by the gate handler at execution time
            depends_on=DEPENDENCIES.get(NodeId.EXECUTIVE_GATE.value, []),
            is_gate=True,
        )
    )
    for node_id in (NodeId.STAKEHOLDER_COORDINATION, NodeId.EXECUTIVE_BRIEFING):
        nodes.append(
            Node(
                node_id.value,
                _agent_executor(node_id),
                depends_on=DEPENDENCIES.get(node_id.value, []),
            )
        )

    return Orchestrator(nodes)


def signal_from_dict(payload: dict[str, Any]) -> DisruptionSignal:
    return DisruptionSignal(
        ingredient_id=payload.get("ingredientId", ""),
        ingredient_name=payload.get("ingredientName", ""),
        supplier_id=payload.get("supplierId", ""),
        confidence=float(payload.get("confidence", 0.0) or 0.0),
        depletion_days_min=int(payload.get("depletionDaysMin", 0) or 0),
        depletion_days_max=int(payload.get("depletionDaysMax", 0) or 0),
        impacted_skus=list(payload.get("impactedSkus") or []),
        affected_regions=list(payload.get("affectedRegions") or []),
        affected_plants=list(payload.get("affectedPlants") or []),
        source=payload.get("source", "databricks-stub"),
        detected_at=payload.get("detectedAt", ""),
    )


GATE_HANDLER = _make_gate_handler()
