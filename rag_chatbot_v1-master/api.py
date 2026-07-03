import os

# Must happen before src.models.llm (and therefore transformers/huggingface_hub)
# gets imported below — otherwise HF tries to hit the network to check for
# model updates and the whole import fails/hangs on an offline machine.
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.ingestion.loader import DocumentLoader
from src.chunking.chunking import RecursiveChunker
from src.embedding.embedding import Embedding
from src.vectorstore.vectore_store import VectorStore
from src.retrieval.vector.faiss_retriever import SearchFaiss
from src.models.llm import LLM

app = FastAPI()

MODEL_PATH = "../rag_chatbot/LLM/phi-3-mini"

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

# The LLM (phi-3-mini) is the slowest thing to load, so we only load it the
# first time someone actually asks a question, not at server startup.
llm = None

def get_llm():
    global llm
    if llm is None:
        llm = LLM(model_path=MODEL_PATH)
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

    prompt = f"""You are a helpful assistant. Answer the question based only on the context provided below.

            Context:{context}
            Question:{req.question}
            Answer:"""

    model = get_llm()
    answer = model.generate(prompt)

    return {"answer": answer}