import pandas as pd


class MovieMapper:
    def __init__(self, movies_path:str):
        self.movies_df = pd.read_csv(movies_path)


        self.movies_df["title_norm"] = (
            self.movies_df["title"].str.lower().str.strip()
        )


        self.id_to_movie = (
            self.movies_df.set_index("id").to_dict(orient="index")
        )

        self.title_to_id = dict(
            zip(self.movies_df["title_norm"],
                self.movies_df["id"])
        )


    def get_movie_by_id(self,movie_id:int)-> dict:
        movie = self.id_to_movie.get(movie_id)

        if not movie:
            raise ValueError(f"Movie ID {movie_id} not found")
        return movie
    
    def get_movie_id_by_title(self, title:str)->int:
        title_norm = title.lower().strip()

        movie_id = self.title_to_id.get(title_norm)

        if movie_id is None:
            raise ValueError(f"Movie title '{title}' not found")
        return movie_id
    

    def get_title_by_ids(self,movie_id:int)->str:
        movie  =self.get_movie_by_id(movie_id)
        return movie["title"]
    

    def get_movies_by_ids(self,movie_ids:list)->list:
        return [self.get_movie_by_id(mid) for mid in movie_ids]
    

    def title_to_movies_dicts(titles,movies_df):

        moviess = movies_df.copy()
        movies = (
            movies_df[moviess["title"].isin(titles)].drop_duplicates("title")
        )
        return movies.to_dict(orient="records")
    

    
    

    
