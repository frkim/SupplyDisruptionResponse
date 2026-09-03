import type { DisruptionSignal, OrchestrationGraph } from '../types';

/**
 * Topology used before `/api/scenario` answers — and if it never answers.
 * The backend is authoritative; these coordinates simply keep the console
 * legible when it is offline.
 */
export const FALLBACK_GRAPH: OrchestrationGraph = {
  nodes: [
    { id: 'signal_normalizer', label: 'Signal Normalizer', description: 'Normalises the inbound Databricks disruption signal.', hostingMode: 'system', group: 'detection', row: 0, col: 2 },
    { id: 'incident_report', label: 'Incident Report', description: 'Builds the comprehensive incident report.', hostingMode: 'foundry', group: 'situational', row: 1, col: 1 },
    { id: 'historical_knowledge', label: 'Historical Knowledge', description: 'Retrieves prior disruptions and lessons learned.', hostingMode: 'foundry', group: 'situational', row: 1, col: 3 },
    { id: 'financial_impact', label: 'Financial Impact', description: 'Revenue at risk, margin impact, supply-chain cost.', hostingMode: 'local', group: 'impact', row: 2, col: 0 },
    { id: 'operational_impact', label: 'Operational Impact', description: 'Production lines, reallocation, logistics.', hostingMode: 'local', group: 'impact', row: 2, col: 2 },
    { id: 'customer_impact', label: 'Customer Impact', description: 'Key accounts, commitments, promotions.', hostingMode: 'local', group: 'impact', row: 2, col: 4 },
    { id: 'impact_synthesis', label: 'Impact Synthesis', description: 'Consolidates the three impact assessments.', hostingMode: 'foundry', group: 'impact', row: 3, col: 2 },
    { id: 'mitigation_planner', label: 'Mitigation Planner', description: 'Generates candidate remediation scenarios.', hostingMode: 'foundry', group: 'remediation', row: 4, col: 2 },
    { id: 'supply_chain_optimization', label: 'Supply Chain Optimization', description: 'Optimises sourcing, allocation and scheduling.', hostingMode: 'a2a', group: 'validation', row: 5, col: 0 },
    { id: 'financial_risk', label: 'Financial Risk', description: 'Prices the downside of each scenario.', hostingMode: 'a2a', group: 'validation', row: 5, col: 1 },
    { id: 'regulatory_compliance', label: 'Regulatory Compliance', description: 'EU food additive and labelling checks.', hostingMode: 'a2a', group: 'validation', row: 5, col: 3 },
    { id: 'sustainability', label: 'Sustainability', description: 'Sourcing standards and emissions review.', hostingMode: 'a2a', group: 'validation', row: 5, col: 4 },
    { id: 'scenario_evaluation', label: 'Scenario Evaluation', description: 'Scores every option across five dimensions.', hostingMode: 'foundry', group: 'decision', row: 6, col: 2 },
    { id: 'deliberation', label: 'Deliberation', description: 'Cross-agent debate and recommendation.', hostingMode: 'foundry', group: 'decision', row: 7, col: 2 },
    { id: 'executive_gate', label: 'Executive Gate', description: 'Human-in-the-loop approval checkpoint.', hostingMode: 'system', group: 'decision', row: 8, col: 2 },
    { id: 'stakeholder_coordination', label: 'Stakeholder Coordination', description: 'Notifies and tasks the affected functions.', hostingMode: 'foundry', group: 'execution', row: 9, col: 1 },
    { id: 'executive_briefing', label: 'Executive Briefing', description: 'Produces the board-level briefing pack.', hostingMode: 'foundry', group: 'execution', row: 9, col: 3 },
  ],
  edges: [
    { from: 'signal_normalizer', to: 'incident_report' },
    { from: 'signal_normalizer', to: 'historical_knowledge' },
    { from: 'incident_report', to: 'financial_impact' },
    { from: 'incident_report', to: 'operational_impact' },
    { from: 'incident_report', to: 'customer_impact' },
    { from: 'historical_knowledge', to: 'financial_impact' },
    { from: 'historical_knowledge', to: 'operational_impact' },
    { from: 'historical_knowledge', to: 'customer_impact' },
    { from: 'financial_impact', to: 'impact_synthesis' },
    { from: 'operational_impact', to: 'impact_synthesis' },
    { from: 'customer_impact', to: 'impact_synthesis' },
    { from: 'impact_synthesis', to: 'mitigation_planner' },
    { from: 'mitigation_planner', to: 'supply_chain_optimization' },
    { from: 'mitigation_planner', to: 'financial_risk' },
    { from: 'mitigation_planner', to: 'regulatory_compliance' },
    { from: 'mitigation_planner', to: 'sustainability' },
    { from: 'supply_chain_optimization', to: 'scenario_evaluation' },
    { from: 'financial_risk', to: 'scenario_evaluation' },
    { from: 'regulatory_compliance', to: 'scenario_evaluation' },
    { from: 'sustainability', to: 'scenario_evaluation' },
    { from: 'scenario_evaluation', to: 'deliberation' },
    { from: 'deliberation', to: 'executive_gate' },
    { from: 'executive_gate', to: 'stakeholder_coordination' },
    { from: 'executive_gate', to: 'executive_briefing' },
  ],
};

export const FALLBACK_SIGNAL: DisruptionSignal = {
  ingredientId: 'ING-PEC-450',
  ingredientName: 'High-methoxyl pectin',
  supplierId: 'SUP-EU-014',
  confidence: 0.87,
  depletionDaysMin: 12,
  depletionDaysMax: 18,
  impactedSkus: [],
  affectedRegions: ['FR', 'DE', 'BE'],
  affectedPlants: [],
  source: 'databricks-stub',
  detectedAt: '',
};
