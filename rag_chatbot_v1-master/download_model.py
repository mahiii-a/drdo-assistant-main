from sentence_transformers import SentenceTransformer
m = SentenceTransformer('all-MiniLM-L6-v2')
m.save('../rag_chatbot/my_embedding_model')