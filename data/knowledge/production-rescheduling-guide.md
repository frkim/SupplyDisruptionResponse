# Production Rescheduling Guide — Lactovia Chilled Dairy Operations

This guide describes how Lactovia S.A. (HQ Rennes, France) reschedules chilled dairy production across its five plants when an ingredient becomes constrained. It is written for supply planners, plant schedulers and the Supply Chain Director. The worked examples use the reference incident of 2026-09-03, in which supplier SUP-EU-014 "Valencia Pectinas S.A." declared force majeure on high-methoxyl pectin ING-PEC-450, leaving PLANT-FR-01 (Rennes) with 12 days of cover, PLANT-DE-02 (Bremen) with 15 days and PLANT-BE-01 (Ghent) with 18 days, across 14 affected SKUs in France, Germany and Belgium.

## Line architecture: why not every SKU runs on every line

Lactovia operates 14 filling lines: PLANT-FR-01 Rennes (4 lines), PLANT-DE-02 Bremen (3), PLANT-BE-01 Ghent (3), PLANT-FR-03 Lyon (2) and PLANT-ES-01 Zaragoza (2). Lines are not interchangeable because the filling head, the sealing technology and the downstream case packer are format-specific.

| Line type | Formats | Where installed | Typical output |
|---|---|---|---|
| Cup filler | 100 g, 125 g, 4×125 g, 8×125 g | FR-01 (2), DE-02 (2), BE-01 (2), FR-03 (1), ES-01 (1) | 24,000 cups/h |
| Pouch filler | 70 g and 90 g squeeze pouch | FR-01 (1) only | 15,000 pouches/h |
| 1 L carton line | 1 L and 500 mL gable-top | FR-01 (1), DE-02 (1), BE-01 (1), FR-03 (1), ES-01 (1) | 9,000 cartons/h |

The single most important structural constraint in the group is that **the pouch filler at PLANT-FR-01 is the only Kids pouch capability Lactovia owns**. Every Lactovia Kids squeeze-pouch SKU sold in France, Germany and Belgium is filled on that one line. It cannot be substituted by a cup line — the sealing jaws, the spout applicator and the retort-free aseptic transfer are unique to that asset. Any mitigation plan that assumes Kids pouch volume can be pushed to Bremen or Ghent is invalid.

## Changeover economics

Scheduling decisions are dominated by changeover cost, not by run-rate differences. Lactovia uses three standard changeover classes:

| Changeover class | Duration | Lost output cost | Materials cost | Total |
|---|---|---|---|---|
| Flavour only, same format | 1.5 h | ~EUR 1,800 | ~EUR 400 | ~EUR 2,200 |
| Format change (cup size or pack count) | 4–6 h | ~EUR 9,500 | included | ~EUR 9,500 |
| Allergen or organic→conventional | 8 h | ~EUR 16,000 | included | ~EUR 16,000 |

The allergen and organic-to-conventional changeover requires a full clean-in-place (CIP) cycle plus a validated cleaning verification with swab results signed off by Quality. **It cannot be reversed within the same shift.** Once a line has been taken from organic to conventional, returning to organic in the same 8-hour shift is not permitted, because the verification protocol requires a documented rinse-water conductivity and ATP result with a minimum hold before release.

## CIP cycle detail

A standard Lactovia CIP cycle runs: pre-rinse (ambient potable water), caustic circulation at 75 °C, intermediate rinse, acid circulation, final rinse. Total elapsed time is **90 to 150 minutes** depending on circuit length — a short fruit-prep dosing circuit sits at the 90-minute end, a full tank-to-filler circuit at 150 minutes.

The governing campaign rule is: **organic production must run first in a campaign, or must follow a validated full CIP.** There is no third option. This single rule is why organic SKUs are expensive to insert mid-week and why a planner protecting an organic Naturel or Kids SKU must either move it to the head of the campaign or absorb a EUR 16,000 changeover.

## Batch minimums and the incubation constraint

A fermentation tank at Lactovia is 12,000 litres. Below 60 % fill the headspace-to-volume ratio changes enough to produce pH drift and texture inconsistency, so the practical minimum batch is **7,200 litres — roughly 55,000 cups at 125 g**. A planner cannot solve a shortage by running many small batches; the tank floor is hard.

Fermentation itself takes **14–16 hours of incubation**. This makes intraday replanning impossible: a decision taken at 09:00 cannot change what fills the line that afternoon, because the base is already in tank. Lactovia therefore operates a **48-hour frozen schedule horizon**. Everything inside 48 hours is committed.

## Campaign planning and the two-changeover penalty

SKUs sharing a fermentation base are grouped into campaigns to avoid tank changeovers. The consequence is that **breaking a campaign to protect one SKU typically costs two changeovers, not one** — one to exit the campaign and one to re-enter it. A planner who sees "insert one extra run of SKU X, cost EUR 2,200" has usually mis-costed the move by a factor of two.

## Building a constrained-ingredient schedule

When an ingredient is the binding constraint, rank SKUs by **contribution margin per kilogram of the constrained ingredient**, not by revenue. Revenue ranking systematically protects the wrong SKUs.

Worked comparison, using ING-PEC-450:

| SKU | Weekly revenue | Pectin usage | Contribution margin | CM per kg pectin |
|---|---|---|---|---|
| Gourmet Vanilla 4×125 g (flagship) | EUR 148,000 | 62 kg/week | EUR 41,400 | **EUR 668/kg** |
| Pro Plain 500 g | EUR 46,000 | 11 kg/week | EUR 15,600 | **EUR 1,418/kg** |

The flagship generates 3.2× the revenue but ranks below the smaller Pro SKU on the metric that matters, because it consumes 5.6× the pectin. Under a pectin constraint, protecting Pro Plain and de-campaigning Gourmet Vanilla preserves more total margin per remaining kilogram — a counter-intuitive result that revenue-based ranking will always get wrong.

## Overtime, weekend shifts and the replanning horizon

A Saturday shift at PLANT-DE-02 costs approximately **EUR 22,000** and adds **38,000 units**. That is roughly EUR 0.58 per incremental unit before materials — viable to protect a listing or a promotional commitment, uneconomic as routine capacity.

Forward replanning is practical to a maximum of **6 weeks**. Beyond that, customer volume commitments and retailer promotional windows are locked and cannot be moved without commercial renegotiation.

## Approval authority

- **Plant Manager** may approve breaking the frozen schedule up to 24 hours forward.
- **Supply Chain Director** approval is required for any break beyond 24 hours.

## Worked mini-example: stretching PLANT-BE-01 from 18 to 26 days

PLANT-BE-01 (Ghent) holds 18 days of ING-PEC-450 cover as of 2026-09-03, consuming approximately 34 kg/day across its pectin-dependent SKUs.

The action is to de-campaign the two tail SKUs on the Ghent cup lines — Lactovia Naturel Apricot 125 g and Lactovia Gourmet Salted Caramel 4×125 g — which together consume 10.5 kg/day, about 31 % of site pectin draw.

| Item | Value |
|---|---|
| Baseline daily pectin draw | 34 kg/day |
| Draw after de-campaigning two tail SKUs | 23.5 kg/day |
| Cover extended from | 18 days (to 2026-09-21) |
| Cover extended to | **26 days (to 2026-09-29)** |
| Extra days bought | **8 days** |
| Units lost over 26 days | 412,000 cups |
| Changeover cost (2 exits + 2 re-entries, flavour-class) | 4 × EUR 2,200 = **EUR 8,800** |
| Lost contribution margin on the two tail SKUs | EUR 61,800 |

Eight additional days at Ghent for EUR 8,800 of changeover cost and EUR 61,800 of foregone margin is a favourable trade when it moves the depletion date past the arrival of a qualified alternate supply. It is a poor trade if no alternate supply is expected inside 26 days — in that case the de-campaigning only relocates the shortfall, and the correct response is to escalate to the Supply Chain Director for a cross-site reallocation from PLANT-ES-01 or PLANT-FR-03, neither of which is pectin-constrained in this incident.
