from sentence_transformers import SentenceTransformer
import numpy as np
class Embedding:
    def __init__(self):
        self.embedder=SentenceTransformer("../rag_chatbot/my_embedding_model")

    def embed(self,chunks):
        embedded_chunks=self.embedder.encode([chunk.page_content for chunk in chunks],normalize_embeddings=True)
        print(f"Embedded =={len(embedded_chunks)}==")
        return embedded_chunks.astype(np.float32) 

    def embed_query(self, query: str):
        embedded_query = self.embedder.encode(query, normalize_embeddings=True)
        return embedded_query.astype(np.float32) 