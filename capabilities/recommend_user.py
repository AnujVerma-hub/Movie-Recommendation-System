from recommender.collaborative_recommender import recommend_for_user

def recommend_user(user_id, top_k=10):
    df = recommend_for_user(user_id,num_recommmendations=top_k)

    if df is None or df.empty:
        return []
    

    recommendations = []


    for _, row in df.iterrows():
        recommendations.append({
            "title": row.get("title"),
            "rating": row.get("imdb_rating"),
            "genres": row.get("genres"),
            "actors": row.get("actors"),
            "where_to_watch": row.get("where_to_watch"),
            "poster": row.get("poster"),
        })


    return recommendations

