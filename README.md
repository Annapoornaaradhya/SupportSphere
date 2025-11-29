# 💬 SupportSphere – RAG-Powered Customer Support Assistant

SupportSphere is an AI-driven customer-support assistant built using Retrieval-Augmented Generation (RAG).  
It combines a Streamlit chat UI, Pinecone vector search, Sentence Transformers embeddings, and FLAN-T5-Large to deliver fast, accurate, and human-like responses.

---

## ✨ Features

- **RAG-based answers** (Pinecone + MiniLM embeddings)
- **FLAN-T5-Large text generation** for detailed, conversational responses
- **Modern chat UI**
  - Dark theme with user/assistant bubbles
  - “SupportSphere is thinking…” spinner
  - Typing-style effect for the latest bot answer
- **Escalation to human agent** (logs stored in CSV)
- **Data ingestion pipeline** to index customer-support answers in Pinecone
- **FAQ viewer** in sidebar

---

## 🧱 Project Structure

```text
SupportSphere/
├─ app.py                     # Streamlit frontend: UI, chat, typing effect, spinner
├─ rag_pipeline.py            # Retrieval + generation pipeline (Pinecone + FLAN-T5)
├─ ingest_to_pinecone.py      # Encode dataset and upload vectors to Pinecone
├─ config.py                  # App title/tagline, ESCALATION_LOG, FAQS_FILE, etc.
├─ requirements.txt           # Python dependencies
├─ .env                       # Local environment variables (NOT committed)
├─ data/
│   └─ faqs.json              # Optional additional FAQ dataset
├─ logs/
│   └─ escalations.csv        # Auto-generated escalation records
└─ .gitignore                 # Excludes venv, logs, .env, caches, etc.
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/SupportSphere.git
cd SupportSphere
```

### 2. Create and activate a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Your `requirements.txt` should include (at minimum):

```text
streamlit
pandas
python-dotenv
sentence-transformers
transformers
torch
pinecone-client
datasets
```

Add any extra libraries you use.

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```text
PINECONE_API_KEY=your_api_key
PINECONE_REGION=us-east-1
PINECONE_INDEX_NAME=supportsphere-better
PINECONE_NAMESPACE=support
```

---

## 🧭 Ingest Data Into Pinecone

```bash
python ingest_to_pinecone.py
```

---

## ▶️ Run the Chatbot

```bash
streamlit run app.py
```

Access at:

```text
http://localhost:8501
```

---

## 📞 Escalation Logging

Logged to:

```text
logs/escalations.csv
```

---

## 🌐 Deployment (Streamlit Community Cloud)

Add these secrets under **Settings → Secrets**:

```toml
PINECONE_API_KEY = "your_api_key"
PINECONE_REGION = "us-east-1"
PINECONE_INDEX_NAME = "supportsphere-better"
PINECONE_NAMESPACE = "support"
```

---
