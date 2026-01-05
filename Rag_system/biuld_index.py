import pandas as pd 
import numpy as np 
import faiss 
from sentence_transformers import SentenceTransformer
from config import *


def build_document(df):
    docs = []
    for _,row in df.iterrows():
        text = f"""
Title:{row.get("title")}
Genres: {row.get("gnere")}
IMDb Rating : {row.get("imdb_rating")}
Available On : {row.get("where_to_watch")}
Overview: {row.get("overview")}
Cast: {row.get("actors")}
"""
        docs.append(text.strip())

    return docs


def main():
    print("Loading dataset..")

    df =pd.read_csv(DATA_PATH)

    print("Loading embedding model..")
    model = SentenceTransformer(EMBEDDING_MODEL)

    print("Building documents...")
    documents = build_document(df)

    print("Generating embeddings...")
    embeddings = model.encode(documents,show_progress_bar=True, convert_to_numpy=True)


    np.save(EMBEDDINDS_PATH, embeddings)

    print("Creating FAISS index..")

    faiss.normalize_L2(embeddings)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    faiss.write_index(index, FAISS_INDEX_PATH)

    print("index build completed!")


if __name__ =="__main__":
        
    main()


        
