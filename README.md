---
title: DocuMind AI
emoji: 🧠
colorFrom: indigo
colorTo: blue
sdk: docker
pinned: false
---

# DocuMind AI — Intelligent RAG Chatbot

> Ask anything about your PDF — powered by Retrieval-Augmented Generation

---

## Live Demo

**Frontend:** [https://rag-model-fs3cskdnkkf5eqxlzslujn.streamlit.app/](https://rag-model-fs3cskdnkkf5eqxlzslujn.streamlit.app/)

**Backend API:** [https://nikhitha-nikhi12-rag-chatbot.hf.space](https://nikhitha-nikhi12-rag-chatbot.hf.space)

---

## Overview

**DocuMind AI** is an intelligent document assistant that lets you upload any PDF and ask questions about it in natural language. It uses **Retrieval-Augmented Generation (RAG)** to retrieve the most relevant sections from your document and generate accurate, grounded answers.

---

## How It Works

```
PDF Document
      ↓
1. LOAD      → Read and parse the PDF
      ↓
2. CHUNK     → Split into 500-word pieces
      ↓
3. EMBED     → Convert to vectors (HuggingFace)
      ↓
4. STORE     → Save in FAISS vector database
      ↓
─────────────────────────────
User asks: "What is LangChain?"
─────────────────────────────
      ↓
5. SEARCH    → Find top 2 relevant chunks
      ↓
6. GENERATE  → Groq LLaMA generates answer
      ↓
7. RESPOND   → Answer returned to user
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Framework** | FastAPI + Uvicorn |
| **Embeddings** | HuggingFace `all-MiniLM-L6-v2` |
| **Vector Store** | FAISS (Facebook AI Similarity Search) |
| **LLM** | Groq `llama-3.1-8b-instant` |
| **Orchestration** | LangChain |
| **Frontend** | Streamlit |
| **Backend Hosting** | HuggingFace Spaces (Docker) |
| **Frontend Hosting** | Streamlit Cloud |
| **Version Control** | GitHub |

---

## Project Structure

```
rag-chatbot/
├── app/
│   ├── __init__.py
│   ├── config.py          ← loads GROQ_API_KEY
│   ├── main.py            ← FastAPI endpoints
│   └── rag_pipeline.py    ← RAG logic
├── data/
│   └── sample.pdf         ← knowledge base
├── vectorstore/           ← FAISS index (prebuilt)
├── frontend/
│   ├── app.py             ← Streamlit chat UI
│   └── requirements.txt   ← frontend dependencies
├── Dockerfile             ← HuggingFace deployment
├── README.md
└── requirements.txt       ← backend dependencies
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API status check |
| `/ask?question=` | GET | Ask a question about the PDF |
| `/health` | GET | Health check |

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Groq API key from [console.groq.com](https://console.groq.com/keys) |

---

## Local Development

```bash
# Clone the repo
git clone https://github.com/fabpot-glitch/Rag-chatbot.git
cd Rag-chatbot

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Add your GROQ_API_KEY to .env file
echo GROQ_API_KEY=your_key_here > .env

# Run backend (Terminal 1)
uvicorn app.main:app --reload --port 8001

# Run frontend (Terminal 2)
streamlit run frontend/app.py
```

Open: `http://localhost:8501`

---

## Author

**SAKE NIKHITHA**
- GitHub: [@fabpot-glitch](https://github.com/fabpot-glitch)
- HuggingFace: [@Nikhitha-nikhi12](https://huggingface.co/Nikhitha-nikhi12)

---

## License

MIT License — free to use and modify.