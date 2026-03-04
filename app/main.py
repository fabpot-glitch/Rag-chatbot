import os
from fastapi import FastAPI, HTTPException
from app.rag_pipeline import create_vectorstore, load_qa_chain

VECTOR_PATH = "vectorstore"

app = FastAPI(
    title="RAG Chatbot API",
    description="Retrieval-Augmented Generation chatbot over custom PDFs",
    version="1.0.0"
)

# Global QA chain — loaded ONCE at startup
qa_chain = None

@app.on_event("startup")
def startup_event():
    global qa_chain
    if not os.path.exists(VECTOR_PATH):
        print("Vectorstore not found — building now...")
        create_vectorstore()
    else:
        print("Vectorstore already exists — skipping build.")
    print("Loading QA chain...")
    qa_chain = load_qa_chain()
    print("API Ready!")

@app.get("/")
def home():
    return {"message": "RAG API is running 🚀"}

@app.get("/ask")
def ask(question: str):
    if not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    try:
        result = qa_chain.invoke({"query": question})
        return {
            "question": question,
            "answer": result["result"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}