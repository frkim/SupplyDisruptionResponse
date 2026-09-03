# Post-Mortem PM-2024-014: HM-450 Pectin Supply Failure, March–May 2024

## Executive summary

Between 2024-03-11 and 2024-05-28 — 78 calendar days — Lactovia lost its sole supply of high-methoxyl pectin ING-PEC-450 ("High-Methoxyl Pectin HM-450") from SUP-EU-014, Valencia Pectinas S.A. of Valencia, Spain. The interruption was caused by a citrus peel feedstock quality failure at the supplier and was classified severity **high**. Eleven finished SKUs across the Lactovia Naturel, Lactovia Gourmet and Lactovia Kids brands depended on the ingredient, exposing EUR 8,400,000 of revenue over the incident window.

Four mitigations were executed in parallel. Combined, they preserved roughly three quarters of the exposed revenue: actual revenue lost was EUR 2,150,000, or 25.6 percent of the amount at risk. Direct mitigation spend totalled EUR 1,382,000, of which EUR 640,000 was contractual penalty rather than material or logistics cost.

The dominant finding of this post-mortem is not the peel crop. It is that Lactovia had chosen to single-source a functionally critical hydrocolloid with no qualified alternate, and therefore had no fast lever to pull on day one. Every mitigation deployed in 2024 was a mitigation that could only begin *after* the disruption was already visible.

## Timeline

| Date | Event |
| --- | --- |
| 2024-03-11 | SUP-EU-014 notifies Lactovia Procurement of an indefinite suspension of HM-450 shipments. |
| 2024-03-12 | Lactovia confirms ~410 tonnes of Valencian navel-orange peel quarantined by the supplier for elevated pesticide residue. |
| 2024-03-14 | Stock sweep completed: PLANT-FR-01 holds 11 days of cover, PLANT-DE-02 16 days, PLANT-BE-01 19 days. |
| 2024-03-20 | Inventory reallocation from PLANT-ES-01 and PLANT-FR-03 authorised; first transfer leaves 2024-03-21. |
| 2024-03-25 | Emergency spot purchase agreed with SUP-EU-023, Rheinland Hydrocolloids GmbH. |
| 2024-03-28 | Customer allocation policy finally agreed at 78 percent of committed volume — 17 days after notification. |
| 2024-04-13 | First Rheinland delivery lands at PLANT-FR-01, 19 days after order placement. |
| 2024-04-24 | Sensory panel rejects two of three reformulated Lactovia Kids SKUs. |
| 2024-04-25 | Single surviving reformulated SKU released to market, 31 days after reformulation start. |
| 2024-05-28 | SUP-EU-014 resumes normal HM-450 shipments; incident closed. |

## Root cause

The 2024 Valencian navel-orange harvest — the feedstock from which SUP-EU-014 extracts HM-450 — returned pesticide residue levels above the supplier's own inbound acceptance specification. Approximately **410 tonnes of raw peel** were quarantined and subsequently rejected. Because Valencia Pectinas operates a single extraction line fed from a regionally concentrated peel supply, rejection of that volume halted HM-450 extraction outright for eleven weeks while the supplier re-sourced compliant peel and re-validated its line.

The proximate cause was therefore external and agricultural. The organisational root cause was internal: ING-PEC-450 was single-sourced from SUP-EU-014 with no qualified second source, no safety-stock policy calibrated to an eleven-week outage, and no standing allocation rule.

## Mitigations and measured effectiveness

| # | Mitigation | Direct cost (EUR) | Effectiveness (0–100) | Time to effect | Measured outcome |
| --- | --- | --- | --- | --- | --- |
| a | Emergency spot purchase, SUP-EU-023 Rheinland Hydrocolloids | 385,000 | 82 | 19 days | 62 tonnes secured at a 24% price premium; became the backbone of continued production from mid-April. |
| b | Inventory reallocation from PLANT-ES-01 and PLANT-FR-03 to PLANT-FR-01 | 47,000 | 71 | 6 days | Covered a 9-day gap at the most exposed plant; cheapest and fastest lever available. |
| c | Partial reformulation of three Lactovia Kids SKUs onto ING-PEC-220 (LM-220) | 310,000 | 44 | 31 days | Sensory panel rejected two of three; only one SKU reached market. Cost includes re-validation. |
| d | Customer allocation at 78% of committed volume across key accounts | 640,000 | 66 | 17 days to policy | Contained channel damage but incurred contractual penalties; policy debate consumed the first ten days. |

Effectiveness scores are the Supply Continuity Committee's post-incident assessment of how much of the exposed volume each action actually protected, normalised to 100.

## Financial outcome

Revenue at risk over the 78-day window was **EUR 8,400,000**. Revenue actually lost was **EUR 2,150,000**. Total direct mitigation cost was **EUR 1,382,000** (385,000 + 47,000 + 310,000 + 640,000). Net of mitigation spend, the incident cost Lactovia approximately **EUR 3,532,000**, against a counterfactual exposure of EUR 8,400,000 had no action been taken.

The two highest-value-per-euro actions were inventory reallocation (effectiveness 71 for EUR 47,000) and the Rheinland spot buy (effectiveness 82 for EUR 385,000). Reformulation was the worst: EUR 310,000 for effectiveness 44, delivered too late to matter.

## Lessons learned

**Single-sourcing a critical hydrocolloid was the root organisational failure.** HM-450 is functionally load-bearing across eleven SKUs and had exactly one approved source. No mitigation available on 2024-03-11 could have been fast, because none had been pre-positioned.

**Second-source qualification should have started before the crisis, not during it.** Rheinland Hydrocolloids was only usable in 2024 because a partial qualification file already existed; had it not, the 19-day lead to first delivery would have been a 10-week lead. Qualification work performed under crisis conditions is slower, more expensive and more error-prone than the same work performed calmly.

**Reformulation is too slow to be a first-wave mitigation.** Thirty-one days elapsed and a two-thirds sensory rejection rate make reformulation a structural response, not an incident response. It belongs in the resilience roadmap, not the crisis playbook.

**Early, honest customer communication reduced penalty exposure materially.** Accounts contacted in the first week negotiated softer allocation terms than accounts contacted after 2024-03-28. The penalty bill would plausibly have been higher without proactive disclosure.

**The absence of a pre-agreed allocation rule cost ten days.** Commercial, Supply Chain and Finance spent the first ten days of the incident arguing about which accounts to protect rather than executing. The eventual 78 percent rule was defensible; it simply arrived far too late.

## Recommendations not yet implemented

Three recommendations from PM-2024-014 remain open as of 2026-09-03.

1. **Dual-source ING-PEC-450 with a standing volume commitment.** Approved in principle in June 2024; no second source has been contracted for baseline volume. SUP-EU-023 remains qualified but holds no Lactovia commitment and has limited capacity.
2. **Establish a standing allocation policy with pre-agreed customer tiers.** Drafted in 2024, never ratified. The 78 percent rule was never codified as policy.
3. **Raise strategic safety stock on critical hydrocolloids to 45 days at the three highest-exposure plants.** Deferred on working-capital grounds. Current cover at PLANT-FR-01, PLANT-DE-02 and PLANT-BE-01 remains well below that target.

## Relevance to a recurrence

A future ING-PEC-450 disruption should invert the 2024 sequence. Inventory reallocation and a spot purchase from an already-qualified source are the only two levers that acted inside 20 days in 2024, and they should be initiated on day one in parallel, not sequentially. The customer allocation rule should be applied from a pre-existing policy rather than negotiated live. Reformulation onto ING-PEC-220 should be scoped only as a structural fallback for non-Kids lines, given the 2024 sensory rejection record, and should never be counted on to relieve pressure inside the first month.

Most importantly, any recurrence will find Lactovia in materially the same structural position as 2024 — single-sourced, thin on cover, and without a ratified allocation rule — because the three principal recommendations of PM-2024-014 were not implemented.
