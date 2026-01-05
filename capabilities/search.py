GENRE_ALIASES = {
     "sci-fi":"science fiction",
     "romantic":"romance",
     "rom-com":"romance",
     "sci fi":"science fiction",
     "scifi": "science fiction"
}




GENRES = [
    "action","adventure","comedy","drama","crime","thriller","romance","horror","science fiction","sci-fi","fantasy","mystery","animation"

]



def extract_genre(query:str):
    q = query.lower()

    for alias, canonical in GENRE_ALIASES.items():
        if alias in q:
            return canonical
    for g in GENRES:
        if g in q:
            return g
        
    return None




def search_movie(query,movies_df,limit=5):
    if not query or movies_df.empty:
        return []
    
    query = query.lower().strip()
    genre = extract_genre(query)


    if "title" not in movies_df.columns:
        raise ValueError("Dataset must contain 'title' column")
    
    cols = ["title"]
    for col in ["id","imdb_rating","genres","poster_path"]:
        if col in movies_df.columns:
            cols.append(col)

    if genre and "genres" in movies_df.columns:
        results = movies_df[movies_df["genres"].str.lower().str.contains(genre,na=False)]


    else:
        results = movies_df[movies_df["title"].str.lower().str.contains(query,na=False)].head(limit)[cols]


    if "imdb_rating" in results.columns:
        results = results.sort_values("imdb_rating", ascending = False)

    return results.head(limit)[cols].to_dict(orient = "records")
