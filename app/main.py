import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RAG Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

qa_chain = None

def get_qa_chain():
    global qa_chain
    if qa_chain is None:
        from app.rag_pipeline import load_qa_chain
        qa_chain = load_qa_chain()
    return qa_chain

@app.get("/")
def home():
    return {"status": "RAG Chatbot API is running"}

@app.get("/ask")
def ask(question: str):
    if not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    try:
        chain = get_qa_chain()
        result = chain.invoke({"query": question})
        return {"question": question, "answer": result["result"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "healthy"}