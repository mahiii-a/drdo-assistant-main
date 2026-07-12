import faiss
import pickle
import numpy as np
from langchain_core.documents import Document
from typing import List

class VectorStore:
    def __init__(self,
                 index_path: str = "D:/drdo-assistant-final-frontend/rag_chatbot_v1-master/assets/faiss_index.bin",
                 metadata_path: str = "D:/drdo-assistant-final-frontend/rag_chatbot_v1-master/assets/metadata.pkl"
                 ):
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.index = None
        self.metadata = {}   # dict: {vector_id: {"text":..., "source":..., "page":..., "doc_id":...}}

    def _make_ids(self, doc_id: int, n_chunks: int):
        # e.g. doc_id=7, chunk 3 -> vector id 7000003
        # This gives every document its own private block of up to 1M chunk-ids,
        # so no two documents can ever collide.
        return np.array([doc_id * 1_000_000 + i for i in range(n_chunks)], dtype=np.int64)

    def add_embeddings(self, embeddings, chunks: List[Document], doc_id: int):
        """Embed+store one document's chunks. Creates the index on first use, appends after that."""
        dimension = embeddings.shape[1]

        if self.index is None:
            self.index = faiss.IndexIDMap2(faiss.IndexFlatIP(dimension))

        ids = self._make_ids(doc_id, len(chunks))
        self.index.add_with_ids(embeddings, ids)

        for vid, chunk in zip(ids, chunks):
            self.metadata[int(vid)] = {
                "text": chunk.page_content,
                "source": chunk.metadata.get("source_file", "unknown"),
                "page": chunk.metadata.get("page", 0),
                "doc_id": doc_id
            }

        print(f"added {len(chunks)} chunks for doc_id={doc_id} — total now =={self.index.ntotal}==")
        return self.index

    def remove_document(self, doc_id: int):
        """Remove all vectors belonging to a given document (called on delete)."""
        if self.index is None:
            return 0

        ids_to_remove = np.array(
            [vid for vid, m in self.metadata.items() if m["doc_id"] == doc_id],
            dtype=np.int64
        )
        if len(ids_to_remove) == 0:
            print(f"No vectors found for doc_id={doc_id}")
            return 0

        self.index.remove_ids(ids_to_remove)
        for vid in ids_to_remove:
            del self.metadata[int(vid)]

        print(f"removed {len(ids_to_remove)} vectors for doc_id={doc_id} — total now =={self.index.ntotal}==")
        return len(ids_to_remove)

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)
        print(f"saved index to {self.index_path}")

    def load(self):
        self.index = faiss.read_index(self.index_path)
        with open(self.metadata_path, "rb") as f:
            self.metadata = pickle.load(f)
        print(f"Loaded =={self.index.ntotal}== vectors from disk")
        return self.index, self.metadata