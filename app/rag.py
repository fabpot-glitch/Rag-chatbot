from dotenv import load_dotenv
import os

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ----------------------------
# 1️⃣ Load document
# ----------------------------
loader = TextLoader("data/sample.txt")
documents = loader.load()

# ----------------------------
# 2️⃣ Split text
# ----------------------------
text_splitter = CharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
texts = text_splitter.split_documents(documents)

# ----------------------------
# 3️⃣ Create embeddings
# ----------------------------
embeddings = HuggingFaceEmbeddings()

# ----------------------------
# 4️⃣ Create vector store
# ----------------------------
vectorstore = FAISS.from_documents(texts, embeddings)

retriever = vectorstore.as_retriever()

# ----------------------------
# 5️⃣ Initialize Groq LLM
# ----------------------------
llm = ChatGroq(
    model="mixtral-8x7b-32768",   # ✅ Stable working model
    temperature=0,
    groq_api_key=GROQ_API_KEY
)

# ----------------------------
# 6️⃣ Create RAG chain
# ----------------------------
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever
)

# ----------------------------
# 7️⃣ Ask function
# ----------------------------
def ask_question(question: str):
    return qa_chain.invoke({"query": question})