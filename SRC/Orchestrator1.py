from capabilities.search import search_movie
from capabilities.movie_details import get_movie_details
from capabilities.recommend_item import recommend_similar
from capabilities.recommend_user import recommend_user
from capabilities.explain import explain_movies, explain_rcommendation
from capabilities.chat import movie_chat, global_chat
from capabilities.top_movies import fetch_movies
from SRC.movie_mapper import MovieMapper



_mapper = None

def get_mapper():
    global _mapper
    if _mapper is None:
        _mapper = MovieMapper("datasets/imdb_enriched.csv")

    return _mapper



def build_movie_context(movie_id):
        mapper = get_mapper()
        
        movie = mapper.get_movie_by_id(movie_id)

        if movie is None:
            return None
        

        return {
            "title": movie.get("title"),
            "genres": movie.get("genres"),
            "overview": movie.get("overview"),
            "rating": movie.get("imdb_rating"),
            "director": movie.get("director"),
            "release_year":movie.get("release_date"),
            "keywords":movie.get("keywords"),
            "original_language":movie.get("original_lanaguage"),
            "vote_average":movie.get("vote_average")
        
        }





class MovieOrchestrator:

    def __init__(self,movies_df):
        self.movies_df = movies_df



    

    def home(self,limit):
        top_movies = fetch_movies(
            self.movies_df,
            sort_col="imdb_rating",
            limit=12,
            columns=["id","title","poster_path","imdb_rating","genres"]
        )

        
    

    def search(self, query, limit=5):
        return search_movie(query,self.movies_df,limit)
    

    def movie_page(self,movie_id):
        movie = get_movie_details(movie_id, self.movies_df)

        if not movie:
            raise ValueError(f"Movie with id {movie_id} not found")
        

        

        similar_movies = recommend_similar(movie_id,self.movies_df)


        recommendation_explanation = explain_rcommendation(base_movie=movie, recommended_movies=similar_movies)


        return {
            "movie":movie,
            "similar_movies":similar_movies,
            "why_recommended": recommendation_explanation

        }
    
    def user_recommendation(self,user_id,limit=10):
        return recommend_user(user_id,limit)
    

    def chat(self,message,movie_id=None):
        if movie_id is not None:
            movie_context = build_movie_context(movie_id)

            if movie_context is None:
                return "Movie not found"
            
            return movie_chat(movie_context,message)
        
        return global_chat(message)
    



    
    


    
        