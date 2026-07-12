from src.ingestion.loader import DocumentLoader
from src.chunking.chunking import RecursiveChunker
from src.embedding.embedding import Embedding
from src.vectorstore.vectore_store import VectorStore
from src.retrieval.vector.faiss_retriever import SearchFaiss
from src.models.llm import LLM
from src.models.testing import LLMAsAJudge
from src.testset.testset2 import test_set
import os

def main():
    embedder = Embedding()
    vectordb = VectorStore()

    if os.path.exists(vectordb.index_path) and os.path.exists(vectordb.metadata_path):
        print("Vector Store Found, Loading ...")
        vectordb.load()
    else:
        print("No index yet — upload a document through the app first.")
        return

    print(f"Total vectors formed : {vectordb.index.ntotal}")
    

# def main():
#     INDEX_PATH="D:/drdo-assistant-final-frontend/rag_chatbot_v1-master/assets/faiss_index.bin"
#     METADATA_PATH="D:/drdo-assistant-final-frontend/rag_chatbot_v1-master/assets/metadata.pkl"
#     # MODEL_PATH    = "../rag_chatbot/assets/tiny-llama"
#     embedder=Embedding()
#     vectordb=VectorStore()
#     #index=vectordb.store_embeddings(embeddings)

#     if os.path.exists(INDEX_PATH) and os.path.exists(METADATA_PATH):
#         print("Vector Store Found, Loading ...")
#         vectordb.load()
#     else:
#         loader=DocumentLoader()
#         text=loader.load_data("../rag_chatbot/assets/sample_manual.pdf") #add the path 

#         chunker=RecursiveChunker()
#         chunks=chunker.chunking(text)

        
#         embeddings=embedder.embed(chunks)
#         index=vectordb.store_embeddings(embeddings,chunks)
#         vectordb.save()
    
#     print(f"Total vectors formed : {vectordb.index.ntotal}")

    #retrieval
    '''
    test_queries=[
        "how to insert the battery",
        "how to attach the camera strap",
        "how to insert a memory card",
        "how to attach a lens to the camera",
        
    ]
    '''

    llm = LLM()
    llm_as_judge = LLMAsAJudge(llm)
    retriever=SearchFaiss(embedder)
    faithfulness_scores = []
    answer_relevance_scores = []
    
    for query in test_set:
        question = query["question"]
        ground_truth = query["answer"]
        results=retriever.search_context(question,vectordb.index,vectordb.metadata)
        #retriever.print_results(question,results)

        context = "\n\n".join([r["text"] for r in results])
        print("\n--- LLM Answer ---")
        answer = llm.generate_answer(query['question'],context)
        print(answer)

        #evaluation
        print("\n--- LLM JUDGE Answer ---")
        judge = llm_as_judge.llm_judge(question, ground_truth, answer, context)
        print(type(judge))
        faithfulness_scores.append(judge["faithfulness"])
        answer_relevance_scores.append(judge["answer_relevance"])
        final_metrics = {
        "faithfulness_avg": sum(faithfulness_scores) / len(faithfulness_scores),
        "answer_relevance_avg": sum(answer_relevance_scores) / len(answer_relevance_scores)
        }
        print(final_metrics)



if __name__ == "__main__":
    main()