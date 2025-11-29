# config.py

import os
from pathlib import Path

# --------- PATHS ---------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"
LOGS_DIR = BASE_DIR / "logs"

FAQS_FILE = DATA_DIR / "faqs.json"
FAISS_INDEX_FILE = VECTORSTORE_DIR / "faiss_index.bin"
METADATA_FILE = VECTORSTORE_DIR / "metadata.json"
ESCALATION_LOG = LOGS_DIR / "escalations.csv"

# Create directories if not exist
for p in [DATA_DIR, VECTORSTORE_DIR, LOGS_DIR]:
    p.mkdir(parents=True, exist_ok=True)

# --------- MODEL NAMES (all free) ---------
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
GENERATIVE_MODEL_NAME = "google/flan-t5-base"

# Retrieval settings
TOP_K = 5
MAX_CONTEXT_CHARS = 2500  # to keep prompt size reasonable

# App
APP_TITLE = "SupportSphere – AI Support Assistant"
APP_TAGLINE = "Resolve FAQs instantly, escalate only when needed."
