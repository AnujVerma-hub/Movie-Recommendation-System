import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
DATA_PATH = "datasets/enriched_movies_platform.csv"
MODEL_DIR  = "models"
VECTORIZED_DATA_PATH = "datasets/vectorized_movies.csv"


os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs("datasets", exist_ok=True)

def load_data(path=DATA_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f" Dataset not found at {path}")
    print(f"Loaded dataset from {path}")
    df = pd.read_csv(path)
    return df

def preprocess_data(df):
    text_cols = ["title", 'overview', 'genre', 'director', 'actors', 'where_to_watch']
    for col in text_cols:
        if col not in df.columns:
            df[col] = ''
        df[col] = df[col].fillna('')


    df["combined_features"] = (
        df['title'] + " " +
        df['overview'] + " " +
        df['genre'] + " " +
        df['director'] + " " +
        df['actors'] + " " +
        df['where_to_watch']
    )

    print(f"Combined text features created")
    return df


def vectorize_text(df, max_features=10000):
    print(f" Crating TF-IDF matrix")
    tfidf = TfidfVectorizer(stop_words='english', max_features=max_features)
    tfidf_matrix = tfidf.fit_transform(df['combined_features'])
    print(f"TF-IDF SHAPE: {tfidf_matrix.shape}")

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    print(f"cosine similarity shape: {cosine_sim.shape}")

    return tfidf, cosine_sim

def save_outputs(df, tfidf, cosine_sim):

    pickle.dump(tfidf, open(os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl"), "wb"))

    pickle.dump(cosine_sim, open(os.path.join(MODEL_DIR, "movie_similarity.pkl"), "wb"))

    df.to_csv(VECTORIZED_DATA_PATH, index=False)
    print(f"All files saved")
    print(f"All models saved")


def main():
    print(f"Startingv movie vectorization")
    df = load_data()
    df = df.head(2000)
    df = preprocess_data(df)
    tfidf, cosine_sim = vectorize_text(df)
    save_outputs(df, tfidf, cosine_sim)
    print(f"Vectorization process completed")

main()
