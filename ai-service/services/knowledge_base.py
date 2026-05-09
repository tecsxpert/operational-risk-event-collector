"""
Knowledge Base Service — Tool-66 AI Microservice
Day 11/12 tasks: Pre-load sentence-transformers at startup and seed ChromaDB with domain knowledge.
Author: AI Developer 1
"""

import os
import logging
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

# Pre-load model at module level so it loads once at startup
MODEL_NAME = "all-MiniLM-L6-v2"
try:
    logger.info("Pre-loading sentence-transformers model: %s", MODEL_NAME)
    embedding_model = SentenceTransformer(MODEL_NAME)
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error("Failed to load sentence-transformers model: %s", e)
    embedding_model = None

# Initialize ChromaDB client
try:
    CHROMA_DATA_DIR = os.getenv("CHROMA_DATA_DIR", "./chroma_data")
    chroma_client = chromadb.PersistentClient(path=CHROMA_DATA_DIR, settings=Settings(anonymized_telemetry=False))
    collection = chroma_client.get_or_create_collection(name="operational_risk_knowledge")
except Exception as e:
    logger.error("Failed to initialize ChromaDB: %s", e)
    collection = None

def seed_knowledge_base():
    """Seed ChromaDB with 10 domain knowledge documents (Day 12)."""
    if collection is None or embedding_model is None:
        logger.warning("Knowledge base dependencies unavailable. Skipping seeding.")
        return

    # Check if already seeded to avoid duplicates
    if collection.count() > 0:
        logger.info("ChromaDB collection already contains %d documents. Skipping seeding.", collection.count())
        return

    logger.info("Seeding ChromaDB with domain knowledge documents...")

    documents = [
        "Internal Fraud: Acts intended to defraud, misappropriate property or circumvent regulations, the law or company policy.",
        "External Fraud: Acts of a third party intended to defraud, misappropriate property or circumvent the law.",
        "Employment Practices and Workplace Safety: Acts inconsistent with employment, health or safety laws or agreements.",
        "Clients, Products, and Business Practice: Unintentional or negligent failure to meet a professional obligation to specific clients.",
        "Damage to Physical Assets: Loss or damage to physical assets from natural disaster or other events.",
        "Business Disruption and Systems Failures: Disruption of business or system failures causing significant downtime.",
        "Execution, Delivery, and Process Management: Failed transaction processing or process management.",
        "Cyber Security Event: Malicious activity targeting IT systems, resulting in data breaches or system unavailability.",
        "Regulatory Compliance Failure: Failure to adhere to legal or regulatory requirements resulting in fines or sanctions.",
        "Third-Party Vendor Risk: Disruption or loss caused by a vendor or service provider failing to deliver as agreed."
    ]

    ids = [f"doc_{i+1}" for i in range(len(documents))]
    
    # Generate embeddings
    embeddings = embedding_model.encode(documents).tolist()

    # Add to collection
    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=ids
    )

    logger.info("Successfully seeded %d documents into ChromaDB.", len(documents))

def query_knowledge_base(query, n_results=3):
    """Retrieve relevant context for a given query."""
    if collection is None or embedding_model is None:
        return []

    try:
        query_embedding = embedding_model.encode([query]).tolist()
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        if results and "documents" in results and results["documents"]:
            return results["documents"][0]
        return []
    except Exception as e:
        logger.error("Error querying knowledge base: %s", e)
        return []
