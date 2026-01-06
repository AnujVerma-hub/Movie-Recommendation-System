import pandas as pd 
import random
from sklearn.metrics.pairwise import cosine_similarity
import re
from scipy.sparse import csr_matrix
import pickle


df = pd.read_csv("datasets/user_ratings_enriched.csv")
print(df.shape)

with open("models/user_similarity_2.pkl","rb") as f:
   user_similarity= pickle.load(f)

with open("models/item_similarity_2.pkl","rb") as f:
    item_similarity = pickle.load(f)
    
required_cols = ["user_id" ,"title", "user_rating"]
if not all(col in df.columns for col in required_cols):
    raise ValueError(f"datsets must contain{required_cols}")
    
user_item_matrix = df.pivot_table(index="user_id",columns="title", values="user_rating",aggfunc='mean').fillna(0)
print("user_item_matrix shape",user_item_matrix.shape)
sparse_matrix = csr_matrix(user_item_matrix.values)

print("type user_similarity_2",type(user_similarity))
print("similar user shape",getattr(user_similarity,"shape","No SHape"))

print("type item_similarity_2",type(item_similarity))
print("similar item shape",getattr(item_similarity,"shape","No SHape"))




user_similarity_df = pd.DataFrame(user_similarity,index=user_item_matrix.index, columns=user_item_matrix.index)
item_similarity_df = pd.DataFrame(item_similarity, index=user_item_matrix.columns, columns=user_item_matrix.columns)

def recommend_for_user(user_id, num_recommmendations=5):
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


