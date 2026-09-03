# Lactovia Customer Allocation Policy — Constrained Supply

Owner: Commercial Direction, Lactovia Group, Rennes. Version 4.2, effective 2026-01-01. Applies to all chilled and ambient dairy SKUs produced at PLANT-FR-01 (Rennes), PLANT-DE-02 (Bremen), PLANT-BE-01 (Ghent), PLANT-FR-03 (Lyon) and PLANT-ES-01 (Zaragoza).

## Allocation is a commercial and legal act

When available supply falls below committed demand, the decision of who is short-shipped is a commercial decision with legal consequences, not a planning convenience. Lactovia sells the same SKUs to retailers that compete directly with one another — CUST-001 Carrefour France against CUST-002 E.Leclerc, CUST-004 REWE Group Germany against CUST-005 EDEKA. Allocating discretionarily between competing customers exposes the group to competition-law challenge under Article 102 TFEU and national equivalents. Every allocation must therefore be produced by a documented, non-discriminatory rule, applied identically to all customers in a tier, and retained for seven years with the input data and the approver's name. Ad-hoc allocation by a National Account Manager is prohibited.

## Customer tiers

| Tier | Definition | Entitlement |
|---|---|---|
| key_account | >EUR 8m annual turnover or strategic listing breadth | Allocation multiplier 1.15; floor 70% of committed volume; phone notification by named NAM; first access to substitute SKUs |
| growth | EUR 2–8m turnover, positive 3-year trajectory | Multiplier 1.00; floor 60%; notification by NAM within 48 hours |
| standard | <EUR 2m or transactional relationship | Multiplier 0.85; floor 60%; notification by Customer Service |

Current key accounts: CUST-001, CUST-002, CUST-004, CUST-005, CUST-007. CUST-009 Sodexo France is foodservice-growth. CUST-011 Colruyt Group is growth, private label.

## The default formula

Allocation is fair-share of available supply weighted by trailing 13-week offtake:

`allocated_i = available_supply × (offtake_i × multiplier_i) ÷ Σ(offtake × multiplier)`

Trailing 13-week offtake — not forecast, not contracted volume — is the denominator, because it is auditable and cannot be inflated by a customer submitting an opportunistic forecast during a shortage. No customer may be cut below 60% of committed volume without written Commercial Director sign-off. No key account may be cut below 70% without Executive Committee sign-off. Both approvals must be recorded before the first short shipment leaves the plant.

## Penalty arithmetic and the decision to breach

A typical Lactovia service-level clause carries a penalty of EUR 0.35 to EUR 1.20 per undelivered unit, plus a service-level rebate of 2–4% of quarterly turnover if fill rate falls below the SLA threshold — commonly 97% for key accounts and 95% for standard. The direct penalty is almost never the material number. A 5,000-unit shortfall at EUR 0.85 costs EUR 4,250 in direct penalty; the same breach on a EUR 6m quarterly account with a 3% rebate clause costs EUR 180,000. Penalty exposure must be computed per customer, in euros, before the allocation is finalised — never after.

The consequence is counter-intuitive and must be respected: it is frequently cheaper to protect a smaller customer carrying a punitive clause than a larger one without. Private-label contracts, of which CUST-011 Colruyt Group is the reference case, typically carry the harshest clauses — per-unit penalties at the top of the range, rebate triggers at 4%, and cost-recovery for the retailer's own promotional waste — while delivering the least brand-equity upside. They are nonetheless expensive to breach.

## Delisting risk

Penalty euros are recoverable; a delisting is not. A retailer that experiences a sustained out-of-stock, typically more than three consecutive weeks on a core facing, can delist the SKU at the next range review. A single delisted SKU at a national retailer costs EUR 400,000 to EUR 2.5m of annualised turnover and takes 18–24 months to recover, against a penalty exposure usually measured in tens of thousands. Allocation scoring therefore weights `delisting_risk` — driven by proximity to the next range review, shelf-space contestability, and whether a competitor product can occupy the facing — alongside penalty euros. Accounts within 90 days of a range review are prioritised.

## Communication protocol — the 48-hour rule

Customers must be informed within 48 hours of the allocation decision and never after they discover the shortfall themselves. Key accounts are called by their named National Account Manager, always by phone before any written communication. Growth and standard accounts are contacted by Customer Service. Every notification must contain: the affected SKUs and brands (Lactovia Naturel, Gourmet, Kids, Pro), the allocated percentage of committed volume, the expected duration in weeks, the recovery date, and the alternative SKU offer. Promising a recovery date that supply cannot support is expressly prohibited; where the date is uncertain, state the confidence interval and the review cadence.

## Promotional interaction

Promotions on constrained SKUs must be suspended. The retailer must be notified at least 21 days before promotion start where the constraint is known that far ahead, and media spend must be formally cancelled or redirected to an unconstrained SKU by written agreement. Running a promotion into an allocation is the single most reliable way to convert a supply problem into a delisting.

## Escalation and authority

| Situation | Approver |
|---|---|
| Allocation above 80% for all customers | Supply Chain Director |
| Any customer 60–80% | Commercial Director |
| Any customer below 60%, or key account below 70% | Executive Committee |
| Deliberate SLA breach with rebate exposure >EUR 250,000 | Executive Committee + CFO |

## Worked example — 62% available supply

Pectin ING-PEC-450 constraint, 2026-09-03. Weekly committed volume equals trailing 13-week offtake. Available supply 59,520 of 96,000 units (62%).

| Customer | Tier | Offtake | Weighted | Allocated | % of commitment | Weekly shortfall | Unit penalty | Weekly penalty | Quarterly rebate exposure |
|---|---|---|---|---|---|---|---|---|---|
| CUST-001 Carrefour France | key | 42,000 | 48,300 | 26,435 | 62.9% | 15,565 | EUR 0.55 | EUR 8,561 | EUR 426,000 (3% of EUR 14.2m) |
| CUST-004 REWE Group | key | 28,000 | 32,200 | 17,623 | 62.9% | 10,377 | EUR 0.85 | EUR 8,820 | EUR 240,000 (2.5% of EUR 9.6m) |
| CUST-007 Delhaize Belgium | key | 15,000 | 17,250 | 9,441 | 62.9% | 5,559 | EUR 0.85 | EUR 4,725 | EUR 96,000 (2% of EUR 4.8m) |
| CUST-011 Colruyt Group | growth | 11,000 | 11,000 | 6,021 | 54.7% | 4,979 | EUR 1.20 | EUR 5,975 | EUR 136,000 (4% of EUR 3.4m) |

Total weekly direct penalty EUR 28,081; total rebate exposure EUR 898,000; combined EUR 926,081. All three key accounts fall below the 70% floor and CUST-011 below the 60% floor, so this distribution requires Executive Committee sign-off before execution.

Blended exposure per unit of shortfall is EUR 28.52 for CUST-011, EUR 27.92 for CUST-001, EUR 23.98 for CUST-004 and EUR 18.12 for CUST-007. The smallest customer is the most expensive to short. Any manual adjustment to the formula output must move volume toward CUST-011 and CUST-001 first, and must be justified in writing against this table.
