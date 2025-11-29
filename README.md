# 💬 SupportSphere – RAG-Powered Customer Support Assistant

SupportSphere is an AI-driven customer-support assistant built using Retrieval-Augmented Generation (RAG).It combines a Streamlit chat UI, Pinecone vector search, Sentence Transformers embeddings, and FLAN-T5-Large to deliver fast, accurate, and human-like responses.

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

## 🧱 Project Structure

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  SupportSphere/  ├─ app.py                     # Streamlit frontend: UI, chat, typing effect, spinner  ├─ rag_pipeline.py            # Retrieval + generation pipeline (Pinecone + FLAN-T5)  ├─ ingest_to_pinecone.py      # Encode dataset and upload vectors to Pinecone  ├─ config.py                  # App title/tagline, ESCALATION_LOG, FAQS_FILE, etc.  ├─ requirements.txt           # Python dependencies  ├─ .env                       # Local environment variables (NOT committed)  ├─ data/  │   └─ faqs.json              # Optional additional FAQ dataset  ├─ logs/  │   └─ escalations.csv        # Auto-generated escalation records  └─ .gitignore                 # Excludes venv, logs, .env, caches, etc.  `

## ⚙️ Setup & Installation

### 1\. Clone the repository

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  git clone https://github.com//SupportSphere.git  cd SupportSphere  `

### 2\. Create and activate a virtual environment

**Windows**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  python -m venv venv  venv\Scripts\activate  `

**Linux / macOS**

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  python3 -m venv venv  source venv/bin/activate  `

### 3\. Install dependencies

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  pip install -r requirements.txt  `

Your requirements.txt should include (at minimum):

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  streamlit  pandas  python-dotenv  sentence-transformers  transformers  torch  pinecone-client  datasets  `

Add any extra libraries you use.

## 🔑 Environment Variables

Create a .env file in the project root:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  PINECONE_API_KEY=your_api_key  PINECONE_REGION=us-east-1  PINECONE_INDEX_NAME=supportsphere-better  PINECONE_NAMESPACE=support  `

These values are used by the ingestion script and the RAG pipeline.

## 🧭 Ingest Data Into Pinecone

Before using the chatbot, build the vector index in Pinecone:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  python ingest_to_pinecone.py  `

This script will:

1.  Load the Bitext customer-support dataset
2.  Chunk long answers into smaller segments
3.  Generate embeddings with SentenceTransformers
4.  Create/check a Pinecone index and upload all vectors

## ▶️ Run the Chatbot

Start the Streamlit app:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  streamlit run app.py  `

Then open your browser at:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  http://localhost:8501  `

You’ll see:

- Hero section with animated tagline and background particles
- Sidebar to choose reply tone (Formal/Friendly) and browse FAQs
- Chat interface with user and SupportSphere bubbles
- Spinner while the model is thinking
- Typing-style appearance of the final answer

## 📞 Escalation Logging

When the user clicks **“Escalate to Human”**, the app appends a row to:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  logs/escalations.csv  `

Each row contains:

- Timestamp
- User email (if provided)
- User question
- Model answer
- Top retrieved documents (as JSON text)

This file can be used by human agents or supervisors to review difficult cases.

## 🌐 Deployment (Streamlit Community Cloud)

1.  Push the project to GitHub.
2.  Go to: [https://share.streamlit.io](https://share.streamlit.io)
3.  Click **New app** and select your repo and branch.
4.  Set the main file to:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  app.py  `

1.  In the app’s **Settings → Secrets**, add:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  PINECONE_API_KEY = "your_api_key"  PINECONE_REGION = "us-east-1"  PINECONE_INDEX_NAME = "supportsphere-better"  PINECONE_NAMESPACE = "support"  `

1.  Deploy. You’ll get a public URL like:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  https://your-username-supportsphere.streamlit.app  `

Use this link for submissions or demos.

## 🤝 Contributing

Contributions are welcome!You can:

- Improve UI/UX
- Tune retrieval & ranking
- Enhance prompts or datasets
- Add new features like auth, analytics, or multi-tenant support

## 📜 License

This project is released under the **MIT License**.
