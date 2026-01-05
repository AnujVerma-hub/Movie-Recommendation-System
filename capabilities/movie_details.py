def get_movie_details(movie_id, movies_df):
    movie = movies_df[movies_df["id"] == movie_id].iloc[0]
    return movie.to_dict()