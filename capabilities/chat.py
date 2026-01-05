from Rag_system.RAG import rag_answer

system_instruction = f"""
You are a movie recommendation assistant.
You are given movie-specific context.
Follow following rules strictly:

Prefer the provided movie context when answering.
If the answer is NOT explicitly present in the context:
- You May use general movie knowledge only for given movie.

Only say "I don't have enough information" IF:
- The question is very specific AND
- Cannot be answered from context or general movie knowledge.

Use general movie knowledge as minimum as you can.

Be concise,fatual, and helpful.
"""

def global_chat(message):

    prompt = f"""
    {system_instruction}

    User question:
    {message}
    """

    return rag_answer(prompt)


    

def movie_chat(movie_context, message):
    prompt = f"""
    {system_instruction}

    Movie Details:
    Title: {movie_context.get("title")}
    genres: {movie_context.get("genres")}
    overview: {movie_context.get("overview")}
    Rating: {movie_context.get("rating")}
    cast: {movie_context.get("cast")}
    Director: {movie_context.get("director")}
    Release_year: {movie_context.get("releases_year")}
    keywords: {movie_context.get("keywords")}
    original_language: {movie_context.get("original_language")}
    vote_average: {movie_context.get("vote_average")}


    User question:
    {message}
    """
    return rag_answer(prompt)

