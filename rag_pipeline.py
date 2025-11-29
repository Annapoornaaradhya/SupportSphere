# rag_pipeline.py

import os
import json
import time
from typing import List, Dict, Tuple

import pandas as pd
from pandas.errors import EmptyDataError
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from transformers import T5ForConditionalGeneration, T5Tokenizer
from pinecone import Pinecone

from config import ESCALATION_LOG

# ------------------ ENV ------------------
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "supportsphere-better")
NAMESPACE = os.getenv("PINECONE_NAMESPACE", "support")
PINECONE_REGION = os.getenv("PINECONE_REGION", "us-east-1")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is not set. Add it to your .env file.")


# ------------------ GENERATOR (FLAN-T5-Large) ------------------

class GeneratorModel:
    """FLAN-T5-Large for long, friendly, step-by-step answers."""

    def __init__(self):
        print("🔵 Loading FLAN-T5-Large...")
        self.tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large")
        self.model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large")

    def generate(self, prompt: str) -> str:
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=768,  # limit input length
        )
        outputs = self.model.generate(
            **inputs,
            max_length=512,     # how long the answer can be
            temperature=0.4,
            top_p=0.9,
            num_beams=4,
            early_stopping=True,
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()


# ------------------ RAG PIPELINE ------------------

class SupportRAGPipeline:
    """
    Retrieval-augmented generation:
    - Use Pinecone + MiniLM to retrieve relevant support snippets
    - Use FLAN-T5-Large to write a detailed, friendly answer
    """

    def __init__(self):
        print("💠 Initializing SupportRAGPipeline...")

        # Embedding model for retrieval (fast + light)
        print("🟢 Loading embedding model for retrieval...")
        self.embedder = SentenceTransformer(
            "sentence-transformers/paraphrase-MiniLM-L3-v2"
        )

        # Pinecone client
        print("🟣 Connecting to Pinecone index...")
        pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index = pc.Index(INDEX_NAME)

        # Generator model
        self.generator = GeneratorModel()

        print("✅ SupportRAGPipeline ready.")

    # --------- RETRIEVAL ---------
    def _retrieve(self, question: str, top_k: int = 5) -> List[Dict]:
        """Retrieve top FAQ chunks from Pinecone."""
        q_vec = self.embedder.encode([question])[0].tolist()

        res = self.index.query(
            namespace=NAMESPACE,
            vector=q_vec,
            top_k=top_k,
            include_metadata=True,
        )

        docs: List[Dict] = []
        for match in res.matches:
            m = match.metadata or {}
            docs.append(
                {
                    "question": m.get("question", ""),
                    "answer": m.get("answer", ""),
                    "row_id": m.get("row_id"),
                    "chunk_id": m.get("chunk_id"),
                    "score": float(match.score),
                }
            )
        return docs

    # --------- CONTEXT BUILDING ---------
    @staticmethod
    def _build_context(docs: List[Dict], max_chars: int = 1200) -> str:
        """
        Build a compact context string from retrieved docs,
        truncated to avoid overflow and truncation in generation.
        """
        pieces = []
        total = 0
        for d in docs:
            text = (d.get("answer") or "").strip()
            if not text:
                continue
            if total + len(text) > max_chars:
                break
            pieces.append(text)
            total += len(text)
        return "\n\n".join(pieces)

    # --------- PROMPT BUILDING (with vertical numbered steps) ---------
    @staticmethod
    def _build_prompt(question: str, context: str, tone: str = "Friendly") -> str:
        """
        Build a clean prompt with strict formatting instructions:
        - Each step MUST appear on a new line.
        - No inline numbering.
        - No merged steps.
        """

        if tone == "Friendly":
            tone_block = (
                "Use a warm, supportive tone with 1–2 emojis maximum. "
                "Write like a helpful, patient customer support specialist."
            )
        else:
            tone_block = (
                "Use a clear, polite and professional tone suitable for business customers. "
                "Do NOT use emojis."
            )

        return f"""
You are **SupportSphere**, an expert customer-support AI assistant.

Write a **clear, friendly, step-by-step answer** to help the customer solve their issue.

STRICT FORMATTING RULES (very important):
- You MUST output steps in this exact vertical format:
    1. First step
    2. Second step
    3. Third step
- Every numbered step MUST be on a **new line**.
- Do NOT write multiple steps on the same line.
- Do NOT merge steps into a single line.
- Do NOT use bullets like "-" or "•". Only use numbered lines (1., 2., 3., ...).
- Keep the numbering continuous (1, 2, 3, 4, ...).

Answer structure:
1. Start with 1–2 short reassuring sentences that show you understand the issue.
2. Then provide **5–8 numbered steps**, each on its own line (as described above).
3. Each step should be short, but clear and actionable.
4. Where useful, briefly explain *why* a step matters.
5. End with a friendly closing sentence offering more help or escalation to a human agent.

Tone instructions:
{tone_block}

Internal support knowledge you can rely on (summarize and rewrite it; do not copy verbatim):

{context}

Customer question:
\"\"\"{question}\"\"\"

Now write the final answer following ALL the formatting rules above,
making sure each numbered step is on its own line.
"""

    # --------- MAIN ANSWER METHOD ---------
    def answer_question(self, question: str, tone: str = "Friendly") -> Tuple[str, List[Dict]]:
        # 1. Retrieve from Pinecone
        docs = self._retrieve(question, top_k=5)

        # 2. Build compact context string
        context = self._build_context(docs)

        # 3. Build prompt and generate detailed answer
        prompt = self._build_prompt(question, context, tone)
        answer = self.generator.generate(prompt)

        return answer, docs


# ------------------ ESCALATION LOGGING ------------------

def log_escalation(
    user_question: str,
    model_answer: str,
    reason: str,
    top_docs: List[Dict],
    user_email: str = "",
) -> None:
    """Append escalation info to CSV log in a robust way."""
    ESCALATION_LOG.parent.mkdir(parents=True, exist_ok=True)

    top_qas = [
        {
            "question": d.get("question", ""),
            "answer": d.get("answer", ""),
            "score": d.get("score", None),
        }
        for d in top_docs
    ]

    row = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "user_email": user_email,
        "user_question": user_question,
        "model_answer": model_answer,
        "reason": reason,
        "top_docs": json.dumps(top_qas, ensure_ascii=False),
    }

    if ESCALATION_LOG.exists() and ESCALATION_LOG.stat().st_size > 0:
        try:
            df = pd.read_csv(ESCALATION_LOG)
        except EmptyDataError:
            df = pd.DataFrame(columns=row.keys())
    else:
        df = pd.DataFrame(columns=row.keys())

    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(ESCALATION_LOG, index=False)
