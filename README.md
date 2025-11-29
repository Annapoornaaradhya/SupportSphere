# SupportSphere – RAG-based AI Support Assistant 💬

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b)
![AI](https://img.shields.io/badge/AI-RAG-purple)
![License](https://img.shields.io/badge/License-MIT-green)

## 1. Overview

**SupportSphere** is an AI-powered Support Assistant designed to automate customer queries using a **Retrieval-Augmented Generation (RAG)** pipeline. It operates on a **local, fully free stack** (no paid APIs or databases required) and features an intelligent escalation mechanism for complex queries.

This project was built as part of the **AI Agent Development Challenge**.

- **Category:** 3 – Sales, Marketing & Support
- **Role:** Support Assistant (Resolve FAQs & escalate complex queries)

## 2. Features 🚀

- **RAG Pipeline:**
  - **Embeddings:** Uses `sentence-transformers/all-MiniLM-L6-v2` for efficient vectorization.
  - **Vector Search:** Implements `FAISS` for fast local similarity search.
  - **Answer Generation:** Utilizes `google/flan-t5-base` for coherent, context-aware responses.
- **Interactive UI (Streamlit):**
  - Dark theme with "Support-style" chat bubbles.
  - Typed.js style typing animations for a realistic feel.
  - Particles.js background effects.
- **FAQ Browser:** Built-in explorer for categories (Account, Billing, Product Usage, Technical Issues).
- **Smart Escalation:** If the AI is unsure or the user requests it, the conversation is logged to a CSV for human agent review.
- **Cost Efficiency:** 100% local and free (no OpenAI/Pinecone costs).

## 3. Tech Stack 🛠️

| Category         | Technology                                   |
| :--------------- | :------------------------------------------- |
| **Language**     | Python 3.x                                   |
| **Frontend**     | Streamlit                                    |
| **LLM / NLP**    | Transformers (Flan-T5), SentenceTransformers |
| **Vector DB**    | FAISS (Facebook AI Similarity Search)        |
| **Data Storage** | JSON (Knowledge Base), CSV (Escalation Logs) |

## 4. Architecture

The system follows a standard RAG workflow:

1.  **Input:** User enters a question in the Streamlit UI.
2.  **Embedding:** The question is embedded using `SentenceTransformer`.
3.  **Retrieval:** The embedding is queried against the `FAISS` vector store to find the top-k relevant FAQ entries.
4.  **Context Construction:** Retrieved FAQs are combined into a context block.
5.  **Generation:** The Context + User Question are passed to the `Flan-T5` model.
6.  **Output:** The generated answer is displayed in the UI.
7.  **Escalation:** If triggered, the query is logged to `escalations.csv`.

```mermaid
graph TD
    A[User Query] --> B[Embedding Model]
    B -->|Vector| C[FAISS Vector Store]
    D[FAQ Knowledge Base] -->|Indexed| C
    C -->|Retrieve Top-k| E[Context]
    A --> F[LLM (Flan-T5)]
    E --> F
    F -->|Generate Answer| G[UI Response]
    G --> H{User Satisfied?}
    H -- No --> I[Escalate to CSV]
    H -- Yes --> J[End Chat]
```

## 5. Directory Structure

```text
support-assistant-ai/
├── app.py                 # Main Streamlit application
├── rag_pipeline.py        # Logic for embeddings, FAISS, and LLM generation
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── data/
│   ├── faq_data.json      # The knowledge base
│   └── escalations.csv    # Log file for escalated queries
└── README.md              # Project documentation
```

## 6. Installation & Local Run 💻

Follow these steps to run the application locally:

### Prerequisites

- Python 3.8 or higher
- Git

### Step-by-Step Instructions

1.  **Clone the repository**

    ```bash
    git clone https://github.com/<your-username>/support-assistant-ai.git
    cd support-assistant-ai
    ```

2.  **Create a Virtual Environment**

    ```bash
    # macOS/Linux
    python -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Dependencies**

    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4.  **Run the App**
    ```bash
    streamlit run app.py
    ```
    The app will open in your browser at `http://localhost:8501`.

## 7. Deployment (Streamlit Cloud) ☁️

To deploy this project for a live demo:

1.  Push your code to a public GitHub repository.
2.  Go to [Streamlit Community Cloud](https://streamlit.io/cloud).
3.  Login with GitHub and click **"New App"**.
4.  Select your repository, branch (`main`), and main file (`app.py`).
5.  Click **"Deploy"**.

## 8. Potential Improvements 🔮

- **Cloud Vector DB:** Switch from local FAISS to Pinecone or ChromaDB for scalability.
- **Context Awareness:** Add chat history memory so the AI remembers previous turns.
- **Sentiment Analysis:** Automatically tag frustrated users for higher priority escalation.
- **Ticketing Integration:** Connect to Zendesk or Jira APIs instead of CSV logging.

---

### Challenge Submission Details

This project fulfills the requirements for **Category 3 (Support Assistant)** by utilizing an equivalent stack to the suggested LangChain workflow, implemented here with pure Transformers and FAISS for a lightweight, controllable local environment.
