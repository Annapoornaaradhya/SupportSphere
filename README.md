# 💬 SupportSphere – AI-Powered Customer Support Assistant (RAG Agent)

SupportSphere is an AI-driven customer support agent built using Retrieval-Augmented Generation (RAG).  
It helps users instantly resolve FAQs using a knowledge base, while escalating complex cases to human agents.  
The agent is designed with a modern UI, typing animations, and configurable reply tone, offering a smooth support experience.

---

## 📌 1. Overview of the Agent

SupportSphere acts as an automated helpdesk assistant.  
When a user asks a question:

1. The question is embedded into vector form.
2. Pinecone retrieves the most relevant support articles.
3. A FLAN-T5 model generates a helpful, conversational answer.
4. The UI displays the response with a typing effect for realism.
5. If needed, users may escalate the issue to human support.

The system reduces support workload while still enabling human intervention when necessary.

---

## ⭐ 2. Features & Limitations

### ✅ **Features**

- **RAG-based Answering**
  - Retrieves top support entries from a Pinecone vector database.
- **Generative Response**
  - FLAN-T5-Large forms complete, friendly answers.
- **Modern Streamlit UI**
  - Dark theme, user & bot chat bubbles  
  - Typing animation for the assistant  
  - “Thinking…” loading spinner  
- **FAQ Category Browser**
  - Users can view sample FAQs by category.
- **Escalation Logging**
  - Logs escalated queries into `logs/escalations.csv`.
- **Tone Selection**
  - Choose “Formal” or “Friendly” reply style.

### ⚠️ **Limitations**

- Requires internet for Pinecone operations (unless using local DB).  
- FLAN-T5-Large can be slow on low-spec machines (no GPU acceleration).  
- Doesn’t currently store conversation context—answers are single-turn.  
- Dataset quality directly affects retrieval quality.  
- No authentication or role-based access in the UI.

---

## 🧰 3. Tech Stack & APIs Used

### **Core Technologies**

| Component | Technology |
|----------|------------|
| UI | Streamlit |
| Embeddings | SentenceTransformers (MiniLM family) |
| Vector Database | Pinecone Serverless |
| Generator Model | FLAN-T5-Large |
| Dataset | Bitext Customer Support Dataset |
| Backend Code | Python |
| Logging | CSV via pandas |
| Environment Management | python-dotenv |

### **APIs Used**

- **Pinecone API**
  - For index creation, vector upsert, similarity search.
- **HuggingFace Transformers API**
  - For FLAN-T5 loading and inference.
- **HuggingFace Datasets API**
  - For loading customer-support training data.

---

## 🛠️ 4. Setup & Run Instructions

### **1. Clone the repository**

```bash
git clone https://github.com/<your-username>/SupportSphere.git
cd SupportSphere
```

---

### **2. Create a virtual environment**

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### **3. Install dependencies**

```bash
pip install -r requirements.txt
```

---

### **4. Add environment variables**

Create a file named `.env`:

```ini
PINECONE_API_KEY=your_api_key
PINECONE_REGION=us-east-1
PINECONE_INDEX_NAME=supportsphere-better
PINECONE_NAMESPACE=support
```

---

### **5. Ingest dataset into Pinecone**

```bash
python ingest_to_pinecone.py
```

---

### **6. Run the app**

```bash
streamlit run app.py
```

Visit:

```text
http://localhost:8501
```

---

## 🚀 5. Potential Improvements

Here are future enhancements that could significantly level up the agent:

### 🔹 Conversation Memory  
Store entire chat context so the assistant can handle multi-turn conversations.

### 🔹 Feedback Loop  
Allow users to mark answers as Helpful or Not Helpful to refine dataset quality.

### 🔹 Admin Dashboard  
Supervisors can view escalations, stats, and retrain the model.

### 🔹 Semantic Query Expansion  
Improve retrieval robustness by enriching user queries.

### 🔹 GPU Acceleration / Model Optimization  
Use quantized FLAN or ONNX runtime for faster responses.

### 🔹 User Authentication  
Allow multiple support agents with different permission levels.

### 🔹 Multi-Language Support  
Embed answers with multilingual models (LaBSE, XLM-R).

---

## 📜 License

This project is licensed under the **MIT License**.

You are free to use, modify, distribute, and sell the software as long as the original copyright notice and this permission notice are included in all copies or substantial portions of the software.
