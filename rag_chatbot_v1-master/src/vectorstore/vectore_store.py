import faiss
import pickle
from langchain_core.documents import Document
from typing import List

class VectorStore:
    def __init__(self,
                 index_path:str="../rag_chatbot/assets/faiss_index.bin",
                 metadata_path:str="../rag_chatbot/assets/metadata.pkl"
                 ):
        self.index_path=index_path
        self.metadata_path=metadata_path
        self.index=None
        self.metadata=None

    def store_embeddings(self,embeddings, chunks: List[Document]):
        dimension=embeddings.shape[1]
        self.index=faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

        self.metadata=[
            {
                "text":chunk.page_content,
                "source":chunk.metadata.get("source_file","unkown"),
                "page":chunk.metadata.get("page",0)
            }
            for chunk in chunks
        ]
        print(f"vector store created with =={self.index.ntotal}== vectors")
        return self.index


    def save(self):
        faiss.write_index(self.index,self.index_path)
        with open(self.metadata_path, "wb") as f:
            # here wb means write binary
            # we are saving the metadata at self.metadata_path
            pickle.dump(self.metadata,f)
        print(f"saved index to {self.index_path}")
    

    def load(self):
        self.index=faiss.read_index(self.index_path)
        with open(self.metadata_path,"rb") as f:
            self.metadata=pickle.load(f)
        print(f"Loaded =={self.index.ntotal}== vectors from disk")
        return self.index,self.metadata