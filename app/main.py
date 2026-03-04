import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

VECTOR_PATH = "vectorstore"
qa_chain = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global qa_chain
    import asyncio
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, startup_tasks)
    yield

def startup_tasks():
    global qa_chain
    from app.rag_pipeline import create_vectorstore, load_qa_chain
    if not os.path.exists(VECTOR_PATH) or not os.listdir(VECTOR_PATH):
        print("Building vectorstore...")
        create_vectorstore()
    print("Loading QA chain...")
    qa_chain = load_qa_chain()
    print("API Ready!")

app = FastAPI(title="RAG Chatbot API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "RAG Chatbot API is running"}

@app.get("/ask")
def ask(question: str):
    if qa_chain is None:
        raise HTTPException(status_code=503, detail="Model is still loading. Try again in a moment.")
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