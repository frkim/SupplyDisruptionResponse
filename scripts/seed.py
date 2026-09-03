"""Seed Cosmos DB containers and the Azure AI Search knowledge index.

Run after provisioning:  python scripts/seed.py
Reads endpoints from the environment (see .env.example) and authenticates with
DefaultAzureCredential, so no keys are required.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from azure.core.exceptions import ResourceExistsError
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

load_dotenv(ROOT / ".env", override=False)

CONTAINERS = {
    "ingredients": ("ingredients.json", "category"),
    "suppliers": ("suppliers.json", "country"),
    "plants": ("plants.json", "country"),
    "products": ("products.json", "brand"),
    "inventory": ("inventory.json", "plantId"),
    "customers": ("customers.json", "region"),
    "commitments": ("commitments.json", "customerId"),
    "promotions": ("promotions.json", "region"),
    "productionSchedule": ("production-schedule.json", "plantId"),
    "pastDisruptions": ("past-disruptions.json", "ingredientId"),
    "playbooks": ("playbooks.json", "category"),
    "stakeholders": ("stakeholders.json", "function"),
    "signals": ("signals.json", "ingredientId"),
}


def seed_cosmos() -> None:
    from azure.cosmos import CosmosClient

    endpoint = os.environ["COSMOS_ENDPOINT"]
    database_name = os.getenv("COSMOS_DATABASE", "SupplyChainDB")

    client = CosmosClient(endpoint, credential=DefaultAzureCredential())
    database = client.get_database_client(database_name)

    total = 0
    for container_name, (filename, _pk) in CONTAINERS.items():
        path = DATA / filename
        if not path.exists():
            print(f"  SKIP {container_name}: {filename} not found")
            continue
        items = json.loads(path.read_text(encoding="utf-8"))
        container = database.get_container_client(container_name)
        written = 0
        for item in items:
            container.upsert_item(item)
            written += 1
        total += written
        print(f"  {container_name}: {written} documents")
    print(f"Cosmos seeding complete: {total} documents.")


def seed_search() -> None:
    from azure.search.documents import SearchClient
    from azure.search.documents.indexes import SearchIndexClient
    from azure.search.documents.indexes.models import (
        SearchableField,
        SearchField,
        SearchFieldDataType,
        SearchIndex,
        SimpleField,
        VectorSearch,
        VectorSearchProfile,
        HnswAlgorithmConfiguration,
    )
    from openai import AzureOpenAI
    from azure.identity import get_bearer_token_provider

    endpoint = os.environ["SEARCH_ENDPOINT"]
    index_name = os.getenv("SEARCH_INDEX_NAME", "disruption-knowledge")
    credential = DefaultAzureCredential()

    index_client = SearchIndexClient(endpoint=endpoint, credential=credential)

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="title", type=SearchFieldDataType.String),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SearchField(
            name="contentVector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=3072,
            vector_search_profile_name="default-profile",
        ),
    ]
    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="default-algorithm")],
        profiles=[
            VectorSearchProfile(
                name="default-profile", algorithm_configuration_name="default-algorithm"
            )
        ],
    )
    index = SearchIndex(name=index_name, fields=fields, vector_search=vector_search)
    try:
        index_client.create_or_update_index(index)
        print(f"  index '{index_name}' ready")
    except ResourceExistsError:
        print(f"  index '{index_name}' already exists")

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    aoai = AzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_ad_token_provider=token_provider,
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
    )
    embedding_model = os.getenv("EMBEDDING_DEPLOYMENT_NAME", "text-embedding-3-large")

    documents = []
    knowledge_dir = DATA / "knowledge"
    for path in sorted(knowledge_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        chunks = _chunk(text)
        for position, chunk in enumerate(chunks):
            documents.append(
                {
                    "id": f"{path.stem}-{position}".replace("_", "-"),
                    "title": path.stem.replace("-", " "),
                    "content": chunk,
                }
            )

    print(f"  embedding {len(documents)} chunks ...")
    for batch_start in range(0, len(documents), 16):
        batch = documents[batch_start : batch_start + 16]
        response = aoai.embeddings.create(
            model=embedding_model, input=[d["content"] for d in batch]
        )
        for doc, item in zip(batch, response.data):
            doc["contentVector"] = item.embedding

    search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)
    search_client.upload_documents(documents=documents)
    print(f"Search seeding complete: {len(documents)} chunks indexed.")


def _chunk(text: str, size: int = 1400) -> list[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""
    for paragraph in paragraphs:
        if len(current) + len(paragraph) + 2 > size and current:
            chunks.append(current)
            current = paragraph
        else:
            current = f"{current}\n\n{paragraph}" if current else paragraph
    if current:
        chunks.append(current)
    return chunks


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    if target in ("all", "cosmos"):
        print("Seeding Cosmos DB ...")
        seed_cosmos()
    if target in ("all", "search"):
        print("Seeding Azure AI Search ...")
        seed_search()
