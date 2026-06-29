from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.ingestion.loader import DocumentLoader
from src.chunking.chunking import RecursiveChunker
from src.embedding.embedding import Embedding
from src.vectorstore.vectore_store import VectorStore
from src.retrieval.vector.faiss_retriever import SearchFaiss
from generator import Generator

app = FastAPI()

# Created ONCE when the server starts — not inside the route function.
# Loading an embedding model on every single request would make each
# call take seconds instead of milliseconds.
embedder = Embedding()
vectordb = VectorStore()
retriever = SearchFaiss(embedder)

try:
    vectordb.load()
    print(f"Loaded index with {vectordb.index.ntotal} vectors")
except Exception:
    print("No index found yet — run main.py first to build one.")

# TinyLlama is the slowest thing to load, so we only load it the first
# time someone actually asks a question, not at server startup.
generator = None

def get_generator():
    global generator
    if generator is None:
        generator = Generator()
    return generator


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"status": "API is running"}


@app.post("/rag/query")
def rag_query(req: ChatRequest):
    if vectordb.index is None or vectordb.index.ntotal == 0:
        raise HTTPException(status_code=400, detail="No documents indexed yet — run main.py first.")

    results = retriever.search_context(req.question, vectordb.index, vectordb.metadata, top_k=5)
    context_chunks = [r["text"] for r in results]

    gen = get_generator()
    answer = gen.generate_answer(req.question, context_chunks)

    return {"answer": answer}