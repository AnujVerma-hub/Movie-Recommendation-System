from recommender.collaborative_recommender import (recommend_for_user,
                                                   recommend_similar_movies)
from Rag_system.RAG import rag_answer
from Rag_system.prompt_builder import format_context

def hybrid_recommend(query_type, query_value,top_k=5):
    if query_type == "user":
        movies_df = recommend_for_user(query_value)
        context = format_context(movies_df)
        movie_title = ",".join(movies_df["title"].tolist())

        prompt = f"""
        You are a movie explanation engine.

        STRICT RULES:
        - Do NOT recommend new movies
        - Do NOT mention movies not listed
        - Use ONLY the provided context


        

        User query:
        {query_value}

        Context:
        {context}

        Task:
        Explain briefly why each movie was recommended.
        """
        explanation = rag_answer(
            prompt
        )

    elif query_type == "item":
        movies_df = recommend_similar_movies(query_value)
        context = format_context(movies_df)
        movie_title = ",".join(movies_df["title"].tolist())

        prompt = f"""
        You are a movie explanation engine.

        STRICT RULES:
        - Do NOT recommend new movies
        - Do NOT mention movies not listed
        - Use ONLY the provided context


        

        User query:
        {query_value}

        Movies:
        {movie_title}

        Context:
        {context}

        Task:
        Explain briefly the plots and synopsis of each movie without MAJOR spoilers in Movies.
        """
        explanation = rag_answer(
            prompt
        )

    else:
        raise ValueError("query type must be 'user" or "item")
    


    return movies_df, explanation



if __name__=="__main__":
    print("Testing Orchestrator...\n")

    movies, explanation = hybrid_recommend(query_type="recommend for me",query_value="user_3",top_k=5)
    

    print("User-based Recommendations:\n")
    for m in movies:
        print("-",m)
    print("\n Explanation:")
    print("\n"+"="* 60+"\n")

    movies, explanation = hybrid_recommend(query_type="movies like",query_value="Interstellar", top_k=5)
    

    print("Similar movies:")
    for m in movies:
        print("-",m)

    print("\n Explanation:")
    print(explanation)