import pandas as pd 
import random
from sklearn.metrics.pairwise import cosine_similarity
import re
from scipy.sparse import csr_matrix
import pickle


_df = None
_user_similarity = None
_item_similarity = None


def get_dataframe():
    global _df
    if _df is None:
        _df = pd.read_csv("datasets/user_ratings_enriched.csv")
    return _df


def get_user_similarity():
    global _user_similarity
    if _user_similarity is None:
        with open("models/user_similarity_2.pkl","rb") as f:
            _user_similarity= pickle.load(f)

    return _user_similarity


def get_item_similarity():
    global _item_similarity
    if _item_similarity is None:
        with open("models/item_similarity_2.pkl","rb") as f:
            _item_similarity = pickle.load(f)

    return _item_similarity









def recommend_for_user(user_id, num_recommmendations=5):
    df = get_dataframe()
    user_similarity = get_user_similarity()
    item_similarity = get_item_similarity()

    required_cols = ["user_id" ,"title", "user_rating"]
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"datsets must contain{required_cols}")
    
    user_item_matrix = df.pivot_table(index="user_id",columns="title", values="user_rating",aggfunc='mean').fillna(0)
    sparse_matrix = csr_matrix(user_item_matrix.values)


    user_similarity_df = pd.DataFrame(user_similarity,index=user_item_matrix.index, columns=user_item_matrix.index)
    item_similarity_df = pd.DataFrame(item_similarity, index=user_item_matrix.columns, columns=user_item_matrix.columns)


    if user_id not in user_similarity_df.index:
        print(f" user {user_id} not found in the dataset")
        return pd.DataFrame()
    
    similar_users = user_similarity_df.loc[user_id].sort_values(ascending=False).iloc[1:num_recommmendations+1].index
    similar_user_ratings = df[df['user_id'].isin(similar_users)]

    avg_ratings = (similar_user_ratings.groupby('title')["user_rating"].mean().sort_values(ascending=False))

    top_titles = avg_ratings.head(num_recommmendations).index.tolist()
    recs = df.drop_duplicates("title")[['title', 'imdb_rating', 'actors', 'where_to_watch', 'poster']]
    recs = recs[recs["title"].isin(top_titles)]
    recs["predicted_rating"] = recs["title"].map(avg_ratings)
    return recs.sort_values(by="predicted_rating",ascending=False)

def recommend_similar_movies(Movie_title, num_recommendatios=5):
    df = get_dataframe()
    user_similarity = get_user_similarity()
    item_similarity = get_item_similarity()

    required_cols = ["user_id" ,"title", "user_rating"]
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"datsets must contain{required_cols}")
    
    user_item_matrix = df.pivot_table(index="user_id",columns="title", values="user_rating",aggfunc='mean').fillna(0)
    sparse_matrix = csr_matrix(user_item_matrix.values)

    user_similarity_df = pd.DataFrame(user_similarity,index=user_item_matrix.index, columns=user_item_matrix.index)
    item_similarity_df = pd.DataFrame(item_similarity, index=user_item_matrix.columns, columns=user_item_matrix.columns)
    if Movie_title not in item_similarity_df.index:
        print(f"{Movie_title} not found in dataset")
        return pd.DataFrame()
    
    similar_scores = item_similarity_df[Movie_title].sort_values(ascending=False)
    top_similar = similar_scores.iloc[1:num_recommendatios+1].index.tolist()

    recs = df.drop_duplicates("title")[['title', 'imdb_rating', 'actors', 'where_to_watch', 'poster']]
    recs = recs[recs["title"].isin(top_similar)]
    recs["similarity_scores"] = recs["title"].map(similar_scores)
    return recs.sort_values(by="similarity_scores", ascending=False)

def interpret_query(query):
    query = query.lower().strip()

    if re.search(r"(like|similar to|movies like|related to)", query):
        for phrase in ["movies like", "similar to", "like", "related to"]:
            if phrase in query:
                movie = query.split(phrase)[-1].strip()
                return "item", movie

    if re.search(r"(recommend for me|based on my history|my suggestions|for me)", query):
        return "user", "user_1"
    
    return None, None

def interactive_query():
    print("\n Unifield collaborative movie Recommender")
    print("Examples")
    print("- movies like inception")
    print("- similar to interstellar")
    print("- recommend for me")


    query = input("Enter your query").strip()
    mode, target = interpret_query(query)

    if mode =="item":
        print(f"\n Finding movies similar to '{target}'..\n")
        recs = recommend_similar_movies(target)
        if recs.empty:
            print("NO similar movies found")
            return
        
        for _,row in recs.iterrows():
            print(f' {row["title"]} -IMDB: {row["imdb_rating"]}')
            print(f' Where: {row["where_to_watch"]}')
            print(f' Actors: {row["actors"]}')
            print(f' Poster: {row["poster"]}\n')

    elif mode == "user":
        print(f"\n Generating personalized recommendations for {target}..\n")
        recs = recommend_for_user(target)
        if recs.empty:
            print("No personalized recommendations found")
            return
        for _,row in recs.iterrows():
            print(f' {row["title"]} -IMDB: {row["imdb_rating"]}')
            print(f' Where: {row["where_to_watch"]}')
            print(f' Actors: {row["actors"]}')
            print(f' Poster: {row["poster"]}\n')
    else:
        print(" Sorry, I didn't understand your query. Try phrases like")
        print(" 'movies like inception' or 'recommmend for me'.")


if __name__ =="__main__":
    interactive_query()


