# Inventory Reallocation Playbook — Lactovia Group

This playbook governs the physical movement of ingredient and finished-goods stock between Lactovia plants: PLANT-FR-01 (Rennes, France), PLANT-DE-02 (Bremen, Germany), PLANT-BE-01 (Ghent, Belgium), PLANT-FR-03 (Lyon, France) and PLANT-ES-01 (Zaragoza, Spain). It is the reference for first-wave mitigation during ingredient disruptions such as the 2026-09-03 force majeure declared by SUP-EU-014 "Valencia Pectinas S.A." on ING-PEC-450 "High-Methoxyl Pectin HM-450".

## When reallocation is the right first move — and when it is not

Reallocation is the fastest lever Lactovia has. It executes in **3–7 days** end to end, carries **low regulatory friction** inside the EU, and needs no supplier qualification, no audit and no artwork. It is the correct first-wave response when the exposure is a **5–15 day gap** between depletion at one site and the arrival of a qualified alternate supply.

Its limitation is absolute: **reallocation never creates supply. It only redistributes it.** Every kilogram moved into a receiving plant is a kilogram removed from a donor plant, and the donor's days of cover falls accordingly. Reallocation is therefore a bridge, not a solution. It buys the time needed for the second wave — alternate sourcing, reformulation, or demand shaping — to land.

Reallocation is the wrong answer when: total network stock is already below aggregate demand (redistribution just relocates the stockout); the gap exceeds ~20 days (the donor cannot sustain it); or the constrained item is finished chilled goods with under 30 days of remaining shelf life (transfer time and requalification consume the residual life).

## The donor protection rule

A donor plant **must retain at least 10 days of cover after transfer**, and **must never fall below its declared safety stock level** for the item. Both conditions must hold. Where they conflict, safety stock wins.

If a proposed transfer would breach either threshold, the transfer is reduced to the largest quantity that satisfies both, or refused. Supply Planning may grant a documented exception down to **7 days of donor cover** only with Plant Manager and Supply Chain Director countersignature, and only when the donor has a confirmed inbound receipt landing inside that window.

## Intra-EU movement: what is and is not required

All five Lactovia sites are inside the EU customs union and the single market, so goods in free circulation move between France, Germany, Belgium and Spain **without any customs entry, import declaration or duty**. There is no border formality to plan around and no broker to engage.

What is still required:

- A **VAT-compliant transfer document** for the intra-Community supply. Movement of own goods between establishments in different Member States is a deemed intra-Community supply/acquisition and must be recorded with both VAT identification numbers, the transfer value, and reporting in the recapitulative statement and Intrastat dispatch/arrival declarations where thresholds are met.
- A **CMR consignment note** for the international road carriage, signed by consignor, carrier and consignee, with copies retained by Logistics.
- **Updated lot traceability records under Regulation (EC) No 178/2002 Article 18** — one-step-back / one-step-forward. Every transferred lot must be traceable from the originating supplier lot through the donor plant's records to the receiving plant's goods-in and onward into finished-product batches. The donor plant's record must show the quantity dispatched, the receiving plant, the date and the transport reference.
- Standard **food-contact and hygiene documentation** for the vehicle: previous-load declaration, cleaning certificate, and for temperature-controlled loads a downloadable datalogger record.

## Ambient hydrocolloids versus chilled finished goods

The two transfer classes behave completely differently, and this drives the mitigation choice.

**Ambient hydrocolloid powders** — ING-PEC-450, ING-PEC-220, ING-GEL-110 and ING-STA-330 — travel **dry at 15–25 °C with humidity control below 60% RH**. They need **no reefer transport**, no cold-chain validation and no temperature excursion protocol. A standard dry curtain-sider or box trailer with an intact roof and a moisture-barrier pallet wrap is sufficient. Pallets must not be stored against external walls in transit and must not be double-stacked above 1,000 kg. This is the single biggest reason **pectin is far easier to reallocate than finished chilled goods**: the transfer is cheap, fast, and carries almost no quality risk.

**Finished chilled goods** require an unbroken **2–6 °C cold chain with continuous temperature logging** at a maximum 5-minute interval. Any **excursion above 8 °C for more than 30 minutes** triggers an automatic quality hold at goods-in and, in practice, **probable write-off** — Lactovia QA releases such loads only on a documented risk assessment with microbiological confirmation, which typically costs more than the load is worth. Loading and unloading must occur at a temperature-controlled dock; the trailer must be pre-cooled to ≤ 4 °C before loading.

## Lane lead times and costs

| Lane | Distance | Transit | Full truck (FTL) cost |
|---|---|---|---|
| PLANT-ES-01 Zaragoza → PLANT-FR-01 Rennes | 1,050 km | 2 days | ~EUR 2,900 |
| PLANT-FR-03 Lyon → PLANT-FR-01 Rennes | 850 km | 1–2 days | ~EUR 2,400 |
| PLANT-FR-01 Rennes → PLANT-BE-01 Ghent | 690 km | 1 day | ~EUR 2,100 |
| PLANT-BE-01 Ghent → PLANT-DE-02 Bremen | 480 km | 1 day | ~EUR 1,700 |
| PLANT-DE-02 Bremen → PLANT-FR-01 Rennes | 1,180 km | 2 days | ~EUR 3,200 |

**Part-load (LTL) pricing** is approximately **EUR 190 per pallet plus a EUR 350 lane minimum**. LTL becomes more expensive than FTL above roughly 13–15 pallets on the longer lanes, so consolidate to FTL where volume permits. A standard Euro-pallet of ING-PEC-450 carries **40 × 25 kg sacks = 1,000 kg**; a full trailer takes 26 pallets, but ambient pectin weight-outs at about **24 tonnes**, so plan **24 pallets per FTL**.

## Lot integrity, splitting and re-labelling

A transfer is executed at **whole-sack granularity**. **Partially consumed 25 kg sacks are not transferable** — once a sack is opened, its remaining contents are committed to the donor plant and must be consumed there within the opened-material window (7 days for hydrocolloids under Lactovia's standard).

Where a supplier lot is split between the donor and the receiving plant, the donor must:

1. Create a **child lot number** derived from the parent supplier lot, preserving the parent reference.
2. **Re-label every pallet** in the split with the child lot, net quantity, original supplier, original manufacture and expiry dates, and the donor plant code.
3. Attach a **copy of the original certificate of analysis** to the transfer file, with the parent lot clearly identified.
4. Record the split in the traceability system on the day of dispatch, not retrospectively.

Failure to re-label a split lot is the most common cause of transfer rejection at goods-in.

## Goods-in requalification at the receiving plant

Transferred material is treated as a new receipt, not as existing stock. The receiving plant performs:

- **Identity check** against the transfer document and pallet labels — 1 hour.
- **Certificate of analysis review** against the item specification (for ING-PEC-450: galacturonic acid ≥ 65%, degree of esterification 68–72%, loss on drying ≤ 12%) — 1–2 hours.
- **Visual and packaging integrity inspection**, including moisture damage and seal integrity — 1 hour.
- **One retained sample** drawn and sealed, held for 12 months beyond finished-product shelf life.
- **Confirmatory laboratory test** where the CoA is incomplete, the parent lot is over 6 months old, or packaging integrity is questioned — **24–48 hours**.

Standard requalification is therefore **24–48 hours** when a confirmatory test is needed. Where the material originates from a Lactovia plant, the parent CoA is complete, and packaging is intact, a **QA-signed positive release compresses this to 4 hours**. Positive release requires the receiving plant QA Manager's signature and is logged as a deviation-free exception; it is not available for third-party material or for any lot with a prior quality hold.

## Shelf life and FEFO

Transfers follow **FEFO** (first expired, first out) at the network level, not the plant level. The rule: **never transfer stock with under 90 days of remaining shelf life, unless the receiving plant will consume it within 14 days** of receipt and Production has confirmed the consuming batch plan in writing.

ING-PEC-450 has a 24-month shelf life from manufacture. Stock older than 18 months is not transferred without a confirmatory functional test (gel strength and DE re-check), because HM pectin gel strength drifts with prolonged storage.

## ERP execution and approvals

The SAP sequence is fixed:

1. **Stock transport order (STO)** raised by Supply Planning against the receiving plant, specifying item, quantity, requested delivery date and the donor plant as supplying site.
2. **Batch determination** at the donor plant selects specific lots under FEFO, respecting the whole-sack and 90-day rules.
3. **Outbound delivery and goods issue** posts the stock out of the donor plant; the CMR and transfer document are generated at this step.
4. **Transfer posting / goods receipt** at the receiving plant places the material into quality-inspection stock, not unrestricted stock.
5. **Usage decision** by receiving-plant QA moves it to unrestricted stock after requalification.

Approval thresholds: **Supply Planning** raises and approves any transfer leaving the donor above 10 days of cover. **Donor Plant Manager** must approve any transfer taking the donor to 7–10 days of cover. **Supply Chain Director** must additionally approve any transfer below 10 days of cover, any transfer above EUR 25,000 in freight cost, and any expedited or dedicated-vehicle booking. **Receiving-plant QA Manager** is the sole approver of positive release.

## Worked example — 18 tonnes of ING-PEC-450, September 2026

**Situation on 2026-09-03.** SUP-EU-014 has declared force majeure. Depletion horizons: PLANT-FR-01 **12 days** (2026-09-15), PLANT-DE-02 **15 days** (2026-09-18), PLANT-BE-01 **18 days** (2026-09-21). SUP-EU-023 "Rheinland Hydrocolloids GmbH" can supply on a **21-day lead time**, so the earliest alternate receipt is approximately **2026-09-24** — leaving a **9-day gap at PLANT-FR-01** and a **3-day gap at PLANT-BE-01**. PLANT-DE-02 is covered by a smaller reallocation not detailed here.

**Donor positions.** PLANT-ES-01 (Zaragoza) holds 34 t of ING-PEC-450 with **41 days of cover** and a safety stock of 6 t. PLANT-FR-03 (Lyon) holds 21 t with **28 days of cover** and a safety stock of 4 t. Neither is currently constrained on pectin because their SKU mix is weighted to ING-PEC-220 and ING-STA-330 formulations.

**Plan.** Move **18 t total**: 12 t from PLANT-ES-01 and 6 t from PLANT-FR-03, allocated 12 t to PLANT-FR-01 and 6 t to PLANT-BE-01.

| Leg | From → To | Quantity | Pallets | Mode | Distance | Transit | Cost |
|---|---|---|---|---|---|---|---|
| A | PLANT-ES-01 → PLANT-FR-01 | 12,000 kg | 12 | FTL | 1,050 km | 2 days | EUR 2,900 |
| B | PLANT-FR-03 → PLANT-FR-01 | 6,000 kg | 6 | FTL | 850 km | 2 days | EUR 2,400 |
| C | PLANT-FR-01 → PLANT-BE-01 | 6,000 kg | 6 | FTL | 690 km | 1 day | EUR 2,100 |

Leg C is a cross-dock: the 6 t from Lyon is received, requalified and re-dispatched from Rennes to Ghent rather than routed direct, because Rennes has the free dock capacity and the combined Lyon–Ghent direct lane would cost more than the two-leg move at this volume.

**Day-by-day timeline.**

| Date | Action |
|---|---|
| 2026-09-03 | STOs raised. Donor cover verified: ES-01 falls 34 t → 22 t (41 → **26 days**); FR-03 falls 21 t → 15 t (28 → **20 days**). Both remain above 10 days and above safety stock. Supply Planning approves; no escalation required. |
| 2026-09-04 | Batch determination and FEFO lot selection at both donors. Whole-sack check passes — no partial sacks included. Child lot numbers created; pallets re-labelled at ES-01 (parent lot split). |
| 2026-09-05 | Goods issue and loading. CMR and intra-Community transfer documents raised for Leg A (ES→FR); Leg B is domestic French, CMR still raised per standard. Dry trailers, 15–25 °C, humidity-controlled wrap. |
| 2026-09-06 | Leg B arrives PLANT-FR-01 (Lyon→Rennes, 2-day transit). Goods-in identity check and CoA review. |
| 2026-09-07 | Leg A arrives PLANT-FR-01 (Zaragoza→Rennes, 2-day transit). Both receipts on QA positive release — parent CoAs complete, packaging intact — released to unrestricted stock in **4 hours**. 6 t reserved for onward Leg C. |
| 2026-09-08 | Leg C dispatched Rennes → Ghent. |
| 2026-09-09 | Leg C arrives PLANT-BE-01. Positive release, 4 hours. Material available to production same day. |

**Cost.** Freight EUR 2,900 + EUR 2,400 + EUR 2,100 = **EUR 7,400**. Handling and re-labelling at approximately EUR 45 per pallet across 24 pallet-movements adds **EUR 1,080**. QA requalification (3 receipt events, positive release) adds approximately **EUR 900**. **Total ≈ EUR 9,380**, or **EUR 0.52 per kg moved** — negligible against the ~18% price premium and the value of 14 SKUs at risk.

**Resulting change in days of cover.**

| Plant | Cover before | Cover after | Alternate supply lands | Gap closed? |
|---|---|---|---|---|
| PLANT-FR-01 | 12 days (to 2026-09-15) | **26 days** (to 2026-09-29) | 2026-09-24 | Yes — 5 days of headroom |
| PLANT-BE-01 | 18 days (to 2026-09-21) | **29 days** (to 2026-10-02) | 2026-09-24 | Yes — 8 days of headroom |
| PLANT-ES-01 (donor) | 41 days | **26 days** | 2026-09-24 | Donor safe, well above 10-day floor |
| PLANT-FR-03 (donor) | 28 days | **20 days** | 2026-09-24 | Donor safe, above 10-day floor |

The reallocation converts a hard stockout at PLANT-FR-01 on 2026-09-15 into a covered position through 2026-09-29, bridging comfortably past the SUP-EU-023 receipt. It does not resolve the disruption — the network is still short in aggregate from October onward — but it removes the immediate production stop and buys the time the sourcing and reformulation workstreams need.
