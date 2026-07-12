import os

# Must happen before src.models.llm / src.embedding.embedding get imported
# below — the embedder (SentenceTransformer) is still HuggingFace-based even
# though the LLM itself now runs through Ollama, so this is still needed to
# stop it from trying to hit the network to check for model updates on an
# offline machine.
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import threading
from src.ingestion.loader import DocumentLoader
from src.chunking.chunking import RecursiveChunker
from src.embedding.embedding import Embedding
from src.vectorstore.vectore_store import VectorStore
from src.retrieval.vector.faiss_retriever import SearchFaiss
from src.models.llm import LLM

app = FastAPI()

# Ollama model tag — must match exactly what `ollama list` shows after
# `ollama create qwen3 -f Modelfile`. Ollama defaults to the ":latest" tag
# if you don't specify one, so "qwen3" and "qwen3:latest" usually point to
# the same thing — confirm with `ollama list` before assuming.
MODEL_NAME = "qwen3:latest"

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

# The LLM class now just opens an HTTP connection to a running
# `ollama serve` process (localhost:11434 by default), so there's no
# multi-second local model load anymore. We still lazy-load it on first
# request to keep startup fast and to fail gracefully if Ollama isn't
# running yet.
llm = None

def get_llm():
    global llm
    if llm is None:
        llm = LLM(model_name=MODEL_NAME)
    return llm


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
    context = "\n\n".join([r["text"] for r in results])

    try:
        model = get_llm()
        answer = model.generate_answer(req.question, context)
    except Exception as e:
        # Most common causes here: `ollama serve` isn't running, or
        # MODEL_NAME doesn't match a model registered in `ollama list`.
        raise HTTPException(status_code=502, detail=f"LLM call failed: {e}")

    return {"answer": answer}

import threading
from pydantic import BaseModel

index_lock = threading.Lock()  # prevents two requests from mutating FAISS at the same time

loader = DocumentLoader()
chunker = RecursiveChunker()

class IngestRequest(BaseModel):
    filepath: str
    doc_id: int

class DeleteRequest(BaseModel):
    doc_id: int

@app.post("/rag/ingest")
def rag_ingest(req: IngestRequest):
    if not os.path.exists(req.filepath):
        raise HTTPException(status_code=404, detail=f"File not found: {req.filepath}")

    documents = loader.load_data(req.filepath)
    if not documents:
        raise HTTPException(status_code=400, detail="Unsupported or unreadable file type")

    chunks = chunker.chunking(documents)
    embeddings = embedder.embed(chunks)

    with index_lock:
        vectordb.add_embeddings(embeddings, chunks, doc_id=req.doc_id)
        vectordb.save()

    return {
        "status": "success",
        "doc_id": req.doc_id,
        "chunks_added": len(chunks),
        "total_vectors": vectordb.index.ntotal
    }

@app.post("/rag/delete")
def rag_delete(req: DeleteRequest):
    with index_lock:
        removed = vectordb.remove_document(req.doc_id)
        if removed > 0:
            vectordb.save()

    return {"status": "success", "doc_id": req.doc_id, "vectors_removed": removed}