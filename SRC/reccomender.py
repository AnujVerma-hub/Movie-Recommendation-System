import pandas as pd 
import numpy as np
import pickle

with open("models/tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("models/movie_similarity.pkl", "rb") as f:
    cosine_sim = pickle.load(f)


df = pd.read_csv("datasets/vectorized_movies.csv")

GENRES = ["action", "comedy", "drama", "romance", "sci-fi", "thriller", "horror", "crime", "fantasy", "adventure", "animation"]


def get_index_from_title(title):
    matches = df[df["title"].str.lower() == title.lower()]
    if len(matches) == 0:
        return None
    return matches.index[0]

def recommended_similar_movies(movie_title, n=5):
    idx = get_index_from_title(movie_title)
    if idx is None:
        return f" Movie '{movie_title}' not found in dataset"
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key = lambda x: x[1],reverse=True)[1:n+1]
    recommended = df.iloc[[i[0] for i in sim_scores]][["title", "genre", "imdb_rating", "actors", "where_to_watch"]]
    print(f" Becuase you liked *{movie_title.title()}*, You may also like:\n")
    for _,row in recommended.iterrows():

        rating = f"{row['imdb_rating']}" if not pd.isna(row['imdb_rating'])  else ""
        print(f'{row["title"]} ({row["genre"]}) ({row["actors"]}) | {rating} | {row["where_to_watch"]}')
    return recommended

def recommend_by_genre(genre, n=5):
    genre = genre.lower()
    genre_movies = df[df["genre"].str.contains(genre, case=False, na=False)]
    if genre_movies.empty:
        return f" No movies found for genre '{genre}"
    
    if "imdb_rating" in genre_movies.columns:
        genre_movies = genre_movies.sort_values(by="imdb_rating", ascending=False)
    recommended = genre_movies.head(n)[["title", "imdb_rating", "actors", "where_to_watch"]]
    print(f"\n Top {genre.title()} Movies:\n")
    for _,row in recommended.iterrows():
        rating = f" {row['imdb_rating']}" if not pd.isna(row["imdb_rating"]) else ""
        print(f'{row["title"]} {row["actors"]} |  {rating} |  {row["where_to_watch"]}')
    return recommended


def get_recommendation(user_input):
    user_input = user_input.lower().strip()
    similar_keywords = ["similar to", "like", "movies like", "films like"]

    for key in similar_keywords:
        if key in user_input:
            movie_name = user_input.split(key)[-1].strip()
            return recommended_similar_movies(movie_name)
        
    
    for g in GENRES:
        if g in user_input:
            return recommend_by_genre(g)
        
    return recommended_similar_movies(user_input)

if __name__=="__main__":
    print(f" Welcome to cinebot -- Your Movie Recommender!\n")
    query = input(" Enter your query(e.g 'movies like Inception' or 'top action movies'): ")
    get_recommendation(query)



     