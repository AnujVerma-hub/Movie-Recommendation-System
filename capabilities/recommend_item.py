from recommender.collaborative_recommender import recommend_similar_movies
def recommend_similar(movie_id,movies_df,top_k=10):
    base_movie = movies_df[movies_df["id"] == movie_id]

    if base_movie.empty:
        return []
    
    base_movie = base_movie.iloc[0]

    base_gneres = set(str(base_movie["genres"]).split("|"))

    similar_movies = []

    for _,row in movies_df.iterrows():
        if row["id"] == movie_id:
            continue

        row_genres = set(str(row["genres"]).split("|"))
        common_genres = base_gneres.intersection(row_genres)

        if len(common_genres)>0:
            similar_movies.append({
                "id":row["id"],
                "title":row["title"],
                "genres":row["genres"],
                "imdb_rating":row.get("imdb_rating"),
                "poster_path":row.get("poster_path"),
                "score": len(common_genres)
            })


    similar_movies = sorted(
        similar_movies,
        key=lambda x:x["score"],
        reverse=True
    )

    return similar_movies[:top_k]