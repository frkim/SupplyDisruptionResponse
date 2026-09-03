"""Shared contracts: the typed envelope, node identifiers, and streaming event schema.

Every integration point in the solution references this module, so changes here ripple
across the orchestrator, the agents, and the frontend event consumer.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class HostingMode(str, Enum):
    """How an agent is hosted. The solution deliberately demonstrates all three."""

    FOUNDRY = "foundry"
    LOCAL = "local"
    A2A = "a2a"
    SYSTEM = "system"


class NodeState(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    AWAITING = "awaiting"


class NodeId(str, Enum):
    """Stable identifiers for every node in the orchestration graph."""

    SIGNAL_NORMALIZER = "signal_normalizer"
    INCIDENT_REPORT = "incident_report"
    HISTORICAL_KNOWLEDGE = "historical_knowledge"
    FINANCIAL_IMPACT = "financial_impact"
    OPERATIONAL_IMPACT = "operational_impact"
    CUSTOMER_IMPACT = "customer_impact"
    IMPACT_SYNTHESIS = "impact_synthesis"
    MITIGATION_PLANNER = "mitigation_planner"
    SUPPLY_CHAIN_OPTIMIZATION = "supply_chain_optimization"
    FINANCIAL_RISK = "financial_risk"
    REGULATORY_COMPLIANCE = "regulatory_compliance"
    SUSTAINABILITY = "sustainability"
    SCENARIO_EVALUATION = "scenario_evaluation"
    DELIBERATION = "deliberation"
    EXECUTIVE_GATE = "executive_gate"
    STAKEHOLDER_COORDINATION = "stakeholder_coordination"
    EXECUTIVE_BRIEFING = "executive_briefing"


class EventType(str, Enum):
    RUN_STARTED = "run_started"
    NODE_STARTED = "node_started"
    NODE_COMPLETED = "node_completed"
    NODE_FAILED = "node_failed"
    NODE_SKIPPED = "node_skipped"
    GATE_AWAITING = "gate_awaiting"
    RUN_COMPLETED = "run_completed"
    RUN_FAILED = "run_failed"
    LOG = "log"


@dataclass
class ToolCall:
    tool_name: str
    arguments: str | None = None
    result: str | None = None
    duration_ms: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "toolName": self.tool_name,
            "arguments": self.arguments,
            "result": self.result,
            "durationMs": self.duration_ms,
        }


@dataclass
class NodeResult:
    """Output of a single orchestration node."""

    node_id: str
    agent_name: str
    hosting_mode: HostingMode
    state: NodeState = NodeState.PENDING
    input: str = ""
    narrative: str = ""
    structured: dict[str, Any] = field(default_factory=dict)
    tool_calls: list[ToolCall] = field(default_factory=list)
    error: str | None = None
    duration_ms: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodeId": self.node_id,
            "agentName": self.agent_name,
            "hostingMode": self.hosting_mode.value,
            "state": self.state.value,
            "input": self.input,
            "narrative": self.narrative,
            "structured": self.structured,
            "toolCalls": [t.to_dict() for t in self.tool_calls],
            "error": self.error,
            "durationMs": self.duration_ms,
            "promptTokens": self.prompt_tokens,
            "completionTokens": self.completion_tokens,
            "totalTokens": self.total_tokens,
        }


@dataclass
class DisruptionSignal:
    """The inbound signal. Produced today by a stub; later by Databricks."""

    ingredient_id: str
    ingredient_name: str
    supplier_id: str
    confidence: float
    depletion_days_min: int
    depletion_days_max: int
    impacted_skus: list[str] = field(default_factory=list)
    affected_regions: list[str] = field(default_factory=list)
    affected_plants: list[str] = field(default_factory=list)
    source: str = "databricks-stub"
    detected_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "ingredientId": self.ingredient_id,
            "ingredientName": self.ingredient_name,
            "supplierId": self.supplier_id,
            "confidence": self.confidence,
            "depletionDaysMin": self.depletion_days_min,
            "depletionDaysMax": self.depletion_days_max,
            "impactedSkus": self.impacted_skus,
            "affectedRegions": self.affected_regions,
            "affectedPlants": self.affected_plants,
            "source": self.source,
            "detectedAt": self.detected_at,
        }


@dataclass
class RunContext:
    """Run-scoped state. Replaces the reference solution's global mutable collector,
    so concurrent incidents cannot interfere with one another."""

    run_id: str = field(default_factory=lambda: f"run-{uuid.uuid4().hex[:12]}")
    incident_id: str = ""
    signal: DisruptionSignal | None = None
    results: dict[str, NodeResult] = field(default_factory=dict)
    decision: dict[str, Any] | None = None
    started_at: float = field(default_factory=time.time)

    def record(self, result: NodeResult) -> None:
        self.results[result.node_id] = result

    def get(self, node_id: str | NodeId) -> NodeResult | None:
        key = node_id.value if isinstance(node_id, NodeId) else node_id
        return self.results.get(key)

    def structured_of(self, node_id: str | NodeId) -> dict[str, Any]:
        result = self.get(node_id)
        return result.structured if result else {}

    def narrative_of(self, node_id: str | NodeId) -> str:
        result = self.get(node_id)
        return result.narrative if result else ""

    @property
    def total_tokens(self) -> int:
        return sum(r.total_tokens for r in self.results.values())

    def summary(self) -> dict[str, Any]:
        return {
            "runId": self.run_id,
            "incidentId": self.incident_id,
            "totalTokens": self.total_tokens,
            "durationMs": int((time.time() - self.started_at) * 1000),
            "nodes": [r.to_dict() for r in self.results.values()],
            "decision": self.decision,
        }
