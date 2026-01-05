import pandas as pd 
import numpy as np 
import random

enriched = pd.read_csv("datasets/enriched_movies_platform.csv")

col_needed = ["title", "imdb_rating", "actors", "where_to_watch", "poster"]

enriched = enriched[col_needed].dropna(subset=["title"]).drop_duplicates(subset='title')

num_users = 300
user_ids = [f"user_{i}" for i in range(1, num_users+1)]

ratings_data = []
movie_id_counter = 1000

for _,row in enriched.iterrows():
    movie_id_counter +=1
    movie_title = row['title']
    imdb_rating = row.get('imdb_rating', np.nan)
    actors = row.get('actors', '')
    where_to_watch = row.get('where_to_watch', '')
    poster = row.get('poster', '')


    users_who_rated = random.sample(user_ids, random.randint(5, 25))

    for user in users_who_rated:
        if not pd.isna(imdb_rating) and isinstance(imdb_rating, (int, float)):
            base = float(imdb_rating)

        else:
            base = random.uniform(5, 8)

        user_rating = round(min(max(np.random.normal(base, 1), 1), 10), 1)
        ratings_data.append([user, movie_id_counter, movie_title, imdb_rating, actors, where_to_watch, poster, user_rating])


user_ratings_df = pd.DataFrame(
    ratings_data, columns=['user_id', 'movie_id', 'title', 'imdb_rating', 'actors', 'where_to_watch', 'poster', 'user_rating']

)

user_ratings_df.to_csv("datasets/movie_with_user_rating.csv", index=False)

print(f"User ratings dataset created successfully")
print(f"Total rows: {len(user_ratings_df)}")



