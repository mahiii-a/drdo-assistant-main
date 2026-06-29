from langchain_text_splitters import RecursiveCharacterTextSplitter
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document
from typing import List
'''
class SemanticChunker:
    def __init__(self,model_name: str="all-MiniLM-L6-v2",similarity_threshold=0.75, max_sentences_per_chunk=10):
        self.model_name=model_name
        self.model=SentenceTransformer(model_name)
        self.similarity_threshold=similarity_threshold
        self.max_sentences_per_chunk=max_sentences_per_chunk

        def chunk(self,documents):
            all_chunks = []
            for doc in documents:
                text = doc.page_content  # extract text from Document object
                sentences = sent_tokenize(text)
                
                if not sentences:
                    continue
                
                # embed each sentence individually
                embedded = [embeddings.embed_query(sentence) for sentence in sentences]
                
                chunks = []
                current_chunk = [sentences[0]]
                
                for i in range(1, len(sentences)):
                    sim = cosine_similarity([embedded[i-1]], [embedded[i]])[0][0]
                    if sim >= similarity_threshold and len(current_chunk) < max_sentences_per_chunk:
                        current_chunk.append(sentences[i])
                    else:
                        chunks.append(" ".join(current_chunk))
                        current_chunk = [sentences[i]]
                
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                
                all_chunks.extend(chunks)
            
            return all_chunks
        
'''

class RecursiveChunker:
    def __init__(self,chunk_size:int=1000,chunk_overlap:int=200):
        self.chunk_size=chunk_size
        self.chunk_overlap=chunk_overlap
        self.text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n","\n"," ",""]
        )
    
    def chunking(self,documents:List[Document])->List[Document]:
        split_docs=self.text_splitter.split_documents(documents)
        print(f"total chunks created: {len(split_docs)}")
        return split_docs