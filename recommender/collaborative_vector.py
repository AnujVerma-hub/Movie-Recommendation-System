import pandas as pd 
import os 
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from scipy.sparse import csr_matrix

DATA_PATH = "datasets/movie_with_user_rating.csv"
MODEL_DIR = "models"


def load_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found at {path}")
    print(f"Loaded dataset from {path}")
    df = pd.read_csv(path)
    return df

def preprocess_data(df):
    required_cols = ["user_id" ,"title", "user_rating"]
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"datsets must contain{required_cols}")
    
    user_item_matrix = df.pivot_table(index="user_id",columns="title", values="user_rating").fillna(0)
    sparse_matrix = csr_matrix(user_item_matrix.values)

    user_similarity = cosine_similarity(sparse_matrix, dense_output=False)

    item_similarity = cosine_similarity(sparse_matrix.T, dense_output=False)

    return user_similarity, item_similarity


def save_model(user_similarity, item_similarity):

    pickle.dump(user_similarity, open(os.path.join(MODEL_DIR, "user_similarity.pkl"), "wb"))

    pickle.dump(item_similarity, open(os.path.join(MODEL_DIR, "item_similarity.pkl"), "wb"))

    print("All file saved ")



def main():
    print("Starting vectorization")

    df = load_data(DATA_PATH)
    df = df.head(2000)
    user_similarity, item_similarity = preprocess_data(df)

    save_model(user_similarity, item_similarity)

    print(f"Vectorization process completed")


main()








