import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.rag_pipeline import load_qa_chain

app = FastAPI(title="RAG Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading QA chain...")
qa_chain = load_qa_chain()
print("API Ready!")

@app.get("/")
def home():
    return {"status": "RAG Chatbot API is running"}

@app.get("/ask")
def ask(question: str):
    if not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    try:
        result = qa_chain.invoke({"query": question})
        return {"question": question, "answer": result["result"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "healthy"}