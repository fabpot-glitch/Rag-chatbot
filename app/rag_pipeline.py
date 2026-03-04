import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from .config import OPENAI_API_KEY

VECTOR_PATH = "vectorstore"
PDF_PATH    = "data/sample.pdf"

def create_vectorstore():
    print("Loading PDF...")
    loader    = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    print("Splitting into chunks...")
    splitter  = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs      = splitter.split_documents(documents)
    print(f"   {len(docs)} chunks created")
    print("Creating embeddings & saving FAISS index...")
    embeddings  = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(VECTOR_PATH)
    print("Vectorstore saved!")

def load_qa_chain():
    embeddings  = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = FAISS.load_local(
        VECTOR_PATH, embeddings, allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)
    return RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)