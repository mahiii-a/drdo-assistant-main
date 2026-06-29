from src.ingestion.loader import DocumentLoader
from src.chunking.chunking import RecursiveChunker
from src.embedding.embedding import Embedding
from src.vectorstore.vectore_store import VectorStore
from src.retrieval.vector.faiss_retriever import SearchFaiss
import os

def main():
    INDEX_PATH="../rag_chatbot/assets/faiss_index.bin"
    METADATA_PATH="../rag_chatbot/assets/metadata.pkl"

    loader=DocumentLoader()
    text=loader.load_data("../rag_chatbot/assets/sample_manual.pdf") #add the path 

    chunker=RecursiveChunker()
    chunks=chunker.chunking(text)

    embedder=Embedding()
    embeddings=embedder.embed(chunks)

    vectordb=VectorStore()
    #index=vectordb.store_embeddings(embeddings)

    if os.path.exists(INDEX_PATH) and os.path.exists(METADATA_PATH):
        print("Vector Store Found, Loading ...")
        vectordb.load()
    else:
        index=vectordb.store_embeddings(embeddings,chunks)
        vectordb.save()
    
    print(f"Total vectors formed : {vectordb.index.ntotal}")

    #retrieval
    test_queries=[
        "how to insert the battery",
        "how to attach the camera strap",
        "how to insert a memory card",
        "how to attach a lens to the camera",
        
    ]
    retriever=SearchFaiss(embedder)
    for query in test_queries:
        results=retriever.search_context(query,vectordb.index,vectordb.metadata)
        retriever.print_results(query,results)


if __name__ == "__main__":
    main()