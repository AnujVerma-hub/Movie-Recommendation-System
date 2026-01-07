from Rag_system.RAG import rag_answer

def explain_movies(movie_titles,user_query):
    prompt = f"""
    Explain why the following movies are relevant.
    User query: {user_query}
    Movies: {','.join(movie_titles)}
    """
    return rag_answer(prompt)

def explain_rcommendation(base_movie:dict,recommended_movies:list) -> str:
    """
    Explains why the recommended movies are similar to the base movie.
    Does NOT rcommend new movies.
    """

    title = base_movie.get("title","None")
    genres = base_movie.get("geners","None")
    overview = base_movie.get("overview", "None")


    base_block = f"""
    Base Movie:
    Title: {title}
    Genres: {genres}
    Oveview: {overview}

    """



    rec_block = ""
    for i,movie in enumerate(recommended_movies, start=1):
        rec_title = movie.get("title","Unknown")
        rec_block +=f"{i}. {rec_title}\n"
        
    prompt = f"""
    You are a recommendation explanation engine.

    STRICT RULES:
    - DO NOT recommend any new movies
    - DO NOT mention  any movies NOT present in the list
    - ONLY explain the synopsis of movies present in the list
    - If list is empty, clearly say: "No similar movies found"


    {base_block}

    Recommended Movies:
    {rec_block}

    Explain the similarity in movies in themes,genre, tone, and storytelling.
    Write 1-2 short paragraphs.
    Your response must ONLY refer to the movies above.
    """
        

    return rag_answer(prompt)
    
