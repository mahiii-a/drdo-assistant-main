from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List,Dict

class SearchFaiss:
    def __init__(self,embedder):
        self.embedder=embedder
    
    def search_context(self,query: str,index,metadata,top_k:int =5):
        
        query_embedded = self.embedder.embed_query(query)
        # Reshape to 2D array (1, dimension) for FAISS
        query_embedded_2d = np.expand_dims(query_embedded, axis=0)

        # 2. Search using the passed index
        scores,indices=index.search(
            query_embedded_2d,top_k
        )
        results=[]
        
        for rank,(score,idx) in enumerate(zip(scores[0],indices[0])):
            results.append({
                "index":int(idx),
                "rank":rank+1,
                "score":float(score),
                "text":metadata[idx]["text"],
                "source": metadata[idx]["source"],
                "page"  : metadata[idx]["page"]  
                }
            )

        return results
    


    def print_results(self,query:str,results: List[Dict]):
        print(f"\nQuery : {query}")
        print("=============================")

        for result in results:
            print(f"Rank: {result['rank']} | Similarity Score: {result['score']:.4f}")
            print(f"Source: {result['source']} (Page {result['page']})")
            print(f"Text Chunk: {result['text'][:200]}...")
            print("-----------------------------")
