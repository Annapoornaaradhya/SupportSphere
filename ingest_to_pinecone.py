import os
import json
import time
import pandas as pd
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "supportsphere-better")
NAMESPACE = os.getenv("PINECONE_NAMESPACE", "support")

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


# ------------------ LOAD DATASET ------------------
def load_bitext_dataset():
    print("📚 Downloading Bitext Customer Support dataset...")
    ds = load_dataset("bitext/Bitext-customer-support-llm-chatbot-training-dataset")
    df = ds["train"].to_pandas()

    df = df.rename(columns={"instruction": "question", "response": "answer"})
    df = df[["question", "answer"]]
    print(f"Loaded {len(df)} customer-support rows.")
    return df


# ------------------ CLEAN + CHUNK ------------------
def chunk_text(text, chunk_size=500):
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    words = text.split()
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks


def build_chunks(df):
    rows = []

    for i, row in df.iterrows():
        q = row["question"]
        a = row["answer"]

        # chunk long answers
        chunks = chunk_text(a, chunk_size=80)

        for idx, ch in enumerate(chunks):
            rows.append({
                "row_id": i,
                "chunk_id": idx,
                "question": q,
                "answer_chunk": ch
            })

    return pd.DataFrame(rows)


# ------------------ EMBEDDINGS ------------------
def build_embeddings(chunk_df):
    print("🔵 Loading embedding model...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    print("⚙️ Encoding chunks...")
    embeddings = model.encode(
        chunk_df["answer_chunk"].tolist(),
        batch_size=32,
        convert_to_numpy=True
    )

    return embeddings


# ------------------ PINECONE ------------------
def ensure_index():
    pc = Pinecone(api_key=PINECONE_API_KEY)

    print("🟡 Checking Pinecone index...")

    if INDEX_NAME not in pc.list_indexes().names():
        print("🧱 Creating Pinecone index...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region=os.getenv("PINECONE_REGION", "us-east-1")
            )
        )
        time.sleep(10)

    print("✅ Pinecone index ready.")
    return pc.Index(INDEX_NAME)


def ingest_to_pinecone():
    df = load_bitext_dataset()
    chunk_df = build_chunks(df)
    embeddings = build_embeddings(chunk_df)

    index = ensure_index()

    print("📤 Uploading to Pinecone...")
    vectors = []
    for i, row in chunk_df.iterrows():
        meta = {
            "question": row["question"],
            "answer": row["answer_chunk"],
            "row_id": int(row["row_id"]),
            "chunk_id": int(row["chunk_id"])
        }

        vectors.append({
            "id": f"{row['row_id']}-{row['chunk_id']}",
            "values": embeddings[i].tolist(),
            "metadata": meta,
        })

        # batch upload every 200 vectors
        if len(vectors) == 200:
            index.upsert(vectors=vectors, namespace=NAMESPACE)
            vectors = []

    # final upload
    if len(vectors) > 0:
        index.upsert(vectors=vectors, namespace=NAMESPACE)

    print("🎉 Done! Pinecone database updated with improved dataset.")


if __name__ == "__main__":
    ingest_to_pinecone()
