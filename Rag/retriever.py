from Rag_system.config import *
import pandas as pd 
from sentence_transformers import SentenceTransformer
import faiss
def retrieve_docs(DATA_PATH,query,k=TOP_k):

    df = pd.read_csv(DATA_PATH)
    documents = df.to_dict(orient="records")

    embed_model = SentenceTransformer(EMBEDDING_MODEL)
    index = faiss.read_index(FAISS_INDEX_PATH)
    
    q_emb = embed_model.encode([query])
    faiss.normalize_L2(q_emb)

    _,idxs = index.search(q_emb, k)
    return [documents[i] for i in idxs[0]]


