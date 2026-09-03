"""Function tools exposed to the agents.

Each tool has an OpenAI schema plus an async handler that reads real domain data.
Docstrings and schemas matter: the model chooses tools based on them.
"""

from __future__ import annotations

from typing import Any

from ..data import get_repository
from ..knowledge import get_knowledge


async def get_ingredient(ingredient_id: str) -> dict[str, Any]:
    repo = await get_repository()
    return await repo.by_id("ingredients", ingredient_id) or {"error": "not found"}


async def get_supplier(supplier_id: str) -> dict[str, Any]:
    repo = await get_repository()
    return await repo.by_id("suppliers", supplier_id) or {"error": "not found"}


async def find_alternative_suppliers(ingredient_id: str) -> list[dict[str, Any]]:
    repo = await get_repository()
    ingredient = await repo.by_id("ingredients", ingredient_id)
    if not ingredient:
        return []
    candidate_ids = list(ingredient.get("alternateSupplierIds") or [])
    suppliers = await repo.by_ids("suppliers", candidate_ids)
    return [
        {
            "id": s.get("id"),
            "name": s.get("name"),
            "country": s.get("country"),
            "qualificationStatus": s.get("qualificationStatus"),
            "qualificationLeadTimeDays": s.get("qualificationLeadTimeDays"),
            "leadTimeDays": s.get("leadTimeDays"),
            "capacityKgPerMonth": s.get("capacityKgPerMonth"),
            "unitPriceEur": s.get("unitPriceEur"),
            "reliabilityScore": s.get("reliabilityScore"),
            "sustainabilityScore": s.get("sustainabilityScore"),
            "co2KgPerKg": s.get("co2KgPerKg"),
            "certifications": s.get("certifications"),
            "riskFlags": s.get("riskFlags"),
        }
        for s in suppliers
    ]


async def get_inventory_for_ingredient(ingredient_id: str) -> list[dict[str, Any]]:
    repo = await get_repository()
    return await repo.where("inventory", ingredientId=ingredient_id)


async def get_products_using_ingredient(ingredient_id: str) -> list[dict[str, Any]]:
    repo = await get_repository()
    products = await repo.all("products")
    return [p for p in products if ingredient_id in (p.get("ingredients") or [])]


async def get_plants(plant_ids: list[str] | None = None) -> list[dict[str, Any]]:
    repo = await get_repository()
    plants = await repo.all("plants")
    if plant_ids:
        wanted = set(plant_ids)
        plants = [p for p in plants if p.get("id") in wanted]
    return plants


async def get_production_schedule(plant_id: str | None = None) -> list[dict[str, Any]]:
    repo = await get_repository()
    rows = await repo.all("productionSchedule")
    if plant_id:
        rows = [r for r in rows if r.get("plantId") == plant_id]
    return rows[:40]


async def get_customers_for_skus(sku_ids: list[str]) -> list[dict[str, Any]]:
    repo = await get_repository()
    wanted = set(sku_ids)
    customers = await repo.all("customers")
    return [c for c in customers if wanted & set(c.get("skusPurchased") or [])]


async def get_commitments_for_skus(sku_ids: list[str]) -> list[dict[str, Any]]:
    repo = await get_repository()
    wanted = set(sku_ids)
    return [c for c in await repo.all("commitments") if c.get("skuId") in wanted]


async def get_promotions_for_skus(sku_ids: list[str]) -> list[dict[str, Any]]:
    repo = await get_repository()
    wanted = set(sku_ids)
    promos = await repo.all("promotions")
    return [p for p in promos if wanted & set(p.get("skuIds") or [])]


async def get_past_disruptions(ingredient_id: str | None = None) -> list[dict[str, Any]]:
    repo = await get_repository()
    rows = await repo.all("pastDisruptions")
    if ingredient_id:
        matching = [r for r in rows if r.get("ingredientId") == ingredient_id]
        if matching:
            return matching
    return rows


async def get_playbooks(category: str | None = None) -> list[dict[str, Any]]:
    repo = await get_repository()
    rows = await repo.all("playbooks")
    if category:
        filtered = [r for r in rows if r.get("category") == category]
        if filtered:
            return filtered
    return rows


async def get_stakeholders(function: str | None = None) -> list[dict[str, Any]]:
    repo = await get_repository()
    rows = await repo.all("stakeholders")
    if function:
        filtered = [r for r in rows if r.get("function") == function]
        if filtered:
            return filtered
    return rows


async def search_knowledge(query: str) -> list[dict[str, Any]]:
    service = await get_knowledge()
    return await service.search(query, top=4)


def _schema(name: str, description: str, properties: dict[str, Any], required: list[str]) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
                "additionalProperties": False,
            },
        },
    }


_STR = {"type": "string"}
_STR_ARRAY = {"type": "array", "items": {"type": "string"}}

TOOL_REGISTRY: dict[str, tuple[dict[str, Any], Any]] = {
    "get_ingredient": (
        _schema(
            "get_ingredient",
            "Look up a single ingredient by its id, including criticality, lead time and supplier links.",
            {"ingredient_id": _STR},
            ["ingredient_id"],
        ),
        get_ingredient,
    ),
    "get_supplier": (
        _schema("get_supplier", "Look up a supplier by id.", {"supplier_id": _STR}, ["supplier_id"]),
        get_supplier,
    ),
    "find_alternative_suppliers": (
        _schema(
            "find_alternative_suppliers",
            "List qualified and unqualified alternative suppliers for an ingredient with price, lead time, capacity, CO2 and risk flags.",
            {"ingredient_id": _STR},
            ["ingredient_id"],
        ),
        find_alternative_suppliers,
    ),
    "get_inventory_for_ingredient": (
        _schema(
            "get_inventory_for_ingredient",
            "Current stock, days of cover and consumption rate for an ingredient at every plant.",
            {"ingredient_id": _STR},
            ["ingredient_id"],
        ),
        get_inventory_for_ingredient,
    ),
    "get_products_using_ingredient": (
        _schema(
            "get_products_using_ingredient",
            "All finished-goods SKUs whose bill of materials contains the ingredient, with revenue and margin.",
            {"ingredient_id": _STR},
            ["ingredient_id"],
        ),
        get_products_using_ingredient,
    ),
    "get_plants": (
        _schema(
            "get_plants",
            "Manufacturing plants with production lines, capacity and utilization.",
            {"plant_ids": _STR_ARRAY},
            [],
        ),
        get_plants,
    ),
    "get_production_schedule": (
        _schema(
            "get_production_schedule",
            "Scheduled production runs with planned units and ingredient requirements.",
            {"plant_id": _STR},
            [],
        ),
        get_production_schedule,
    ),
    "get_customers_for_skus": (
        _schema(
            "get_customers_for_skus",
            "Customers that purchase any of the given SKUs, with tier and service level agreement.",
            {"sku_ids": _STR_ARRAY},
            ["sku_ids"],
        ),
        get_customers_for_skus,
    ),
    "get_commitments_for_skus": (
        _schema(
            "get_commitments_for_skus",
            "Contractual delivery commitments for the given SKUs including penalties.",
            {"sku_ids": _STR_ARRAY},
            ["sku_ids"],
        ),
        get_commitments_for_skus,
    ),
    "get_promotions_for_skus": (
        _schema(
            "get_promotions_for_skus",
            "Live and planned promotional campaigns covering the given SKUs.",
            {"sku_ids": _STR_ARRAY},
            ["sku_ids"],
        ),
        get_promotions_for_skus,
    ),
    "get_past_disruptions": (
        _schema(
            "get_past_disruptions",
            "Historical disruption records with mitigations applied, effectiveness scores and lessons learned.",
            {"ingredient_id": _STR},
            [],
        ),
        get_past_disruptions,
    ),
    "get_playbooks": (
        _schema(
            "get_playbooks",
            "Mitigation playbooks with steps, typical cost, lead time and required approvals.",
            {"category": _STR},
            [],
        ),
        get_playbooks,
    ),
    "get_stakeholders": (
        _schema(
            "get_stakeholders",
            "Stakeholder directory with role, function, decision authority and escalation level.",
            {"function": _STR},
            [],
        ),
        get_stakeholders,
    ),
    "search_knowledge": (
        _schema(
            "search_knowledge",
            "Retrieve passages from the corporate knowledge corpus: post-mortems, playbooks, regulatory and sustainability guidance.",
            {"query": _STR},
            ["query"],
        ),
        search_knowledge,
    ),
}


def schemas_for(names: list[str]) -> list[dict[str, Any]]:
    return [TOOL_REGISTRY[n][0] for n in names if n in TOOL_REGISTRY]


def handlers_for(names: list[str]) -> dict[str, Any]:
    return {n: TOOL_REGISTRY[n][1] for n in names if n in TOOL_REGISTRY}
