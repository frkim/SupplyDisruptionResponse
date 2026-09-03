import type { NodeResult } from '../types';
import {
  DASH,
  formatCurrencyEur,
  formatNumber,
  pickArray,
  pickNumber,
} from '../lib/format';
import './ImpactDashboard.css';

interface ImpactDashboardProps {
  results: Record<string, NodeResult>;
}

interface MetricSpec {
  key: string;
  label: string;
  hint: string;
  tone: 'money' | 'ops' | 'customer';
  value: string;
  present: boolean;
}

export function ImpactDashboard({ results }: ImpactDashboardProps) {
  const financial = results['financial_impact']?.structured;
  const operational = results['operational_impact']?.structured;
  const customer = results['customer_impact']?.structured;
  const synthesis = results['impact_synthesis']?.structured;

  const revenueAtRisk = firstNumber(
    [financial, synthesis],
    ['revenueAtRisk', 'revenueAtRiskEur', 'revenue_at_risk', 'totalRevenueAtRisk'],
  );
  const marginImpact = firstNumber(
    [financial, synthesis],
    ['marginImpact', 'marginImpactEur', 'margin_impact', 'grossMarginImpact'],
  );
  const supplyChainCost = firstNumber(
    [financial, operational, synthesis],
    ['supplyChainCost', 'supplyChainCostEur', 'supply_chain_cost', 'logisticsCost'],
  );
  const unitsAtRisk = firstNumber(
    [operational, financial, synthesis],
    ['unitsAtRisk', 'units_at_risk', 'volumeAtRisk', 'unitsImpacted'],
  );
  const productionLines = firstCount(
    [operational, synthesis],
    ['productionLinesAffected', 'production_lines_affected', 'affectedProductionLines', 'linesAffected'],
  );
  const keyAccounts = firstCount(
    [customer, synthesis],
    ['keyAccountsAffected', 'key_accounts_affected', 'affectedAccounts', 'keyAccounts'],
  );
  const commitments = firstCount(
    [customer, synthesis],
    ['commitmentsAtRisk', 'commitments_at_risk', 'contractualCommitmentsAtRisk', 'commitments'],
  );

  const metrics: MetricSpec[] = [
    metric('revenue', 'Revenue at risk', 'financial_impact', 'money', formatCurrencyEur(revenueAtRisk), revenueAtRisk !== undefined),
    metric('margin', 'Margin impact', 'financial_impact', 'money', formatCurrencyEur(marginImpact), marginImpact !== undefined),
    metric('scCost', 'Supply-chain cost', 'financial_impact', 'money', formatCurrencyEur(supplyChainCost), supplyChainCost !== undefined),
    metric('units', 'Units at risk', 'operational_impact', 'ops', formatNumber(unitsAtRisk), unitsAtRisk !== undefined),
    metric('lines', 'Production lines affected', 'operational_impact', 'ops', formatNumber(productionLines), productionLines !== undefined),
    metric('accounts', 'Key accounts affected', 'customer_impact', 'customer', formatNumber(keyAccounts), keyAccounts !== undefined),
    metric('commitments', 'Commitments at risk', 'customer_impact', 'customer', formatNumber(commitments), commitments !== undefined),
  ];

  const anyData = metrics.some((m) => m.present);

  return (
    <section className="card">
      <div className="card__head">
        <h2 className="card__title">Business impact</h2>
        {!anyData ? <span className="chip">awaiting assessment</span> : null}
      </div>
      <div className="card__body impact">
        <div className="impact__grid">
          {metrics.map((m) => (
            <div
              key={m.key}
              className={`impact__card impact__card--${m.tone} ${m.present ? '' : 'impact__card--empty'}`}
            >
              <span className="impact__label">{m.label}</span>
              <span className="impact__value">{m.value}</span>
              <span className="impact__hint mono">{m.hint}</span>
            </div>
          ))}
        </div>
        {!anyData ? (
          <p className="impact__note">
            Metrics populate as the financial, operational and customer impact agents report.
          </p>
        ) : null}
      </div>
    </section>
  );
}

function metric(
  key: string,
  label: string,
  hint: string,
  tone: MetricSpec['tone'],
  value: string,
  present: boolean,
): MetricSpec {
  return { key, label, hint, tone, value: present ? value : DASH, present };
}

function firstNumber(sources: Array<unknown>, keys: string[]): number | undefined {
  for (const source of sources) {
    const value = pickNumber(source, keys);
    if (value !== undefined) return value;
  }
  return undefined;
}

/** Counts accept either a number or an array of entities. */
function firstCount(sources: Array<unknown>, keys: string[]): number | undefined {
  for (const source of sources) {
    const arr = pickArray(source, keys);
    if (arr) return arr.length;
    const value = pickNumber(source, keys);
    if (value !== undefined) return value;
  }
  return undefined;
}

export default ImpactDashboard;
