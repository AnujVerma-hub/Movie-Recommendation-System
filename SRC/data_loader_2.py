import pandas as pd
import numpy
import os


def data_cleaner(path_1: str, path_2: str) -> pd.DataFrame:

    tmdb = pd.read_csv(path_1)
    bolly = pd.read_csv(path_2)

    # tmdb cleaning

    tmdb = tmdb.rename(columns={
        'title': 'title',
        'overview': 'overview',
        'original_language': 'language',
        'release_date': 'release_year',
        'vote_average': 'tmdb_rating',
        'id': 'tmdb_id',
        'imdb_id': 'imdb_id'
    })

    tmdb['release_year'] = pd.to_datetime(tmdb['release_year'], errors='coerce').dt.year
    tmdb = tmdb[['title','overview','language','release_year','tmdb_rating','tmdb_id','imdb_id']]


    # bollywood data cleaning
    bolly = bolly.rename(columns={
        'movie_name': 'title',
        'year': 'release_year',
        'director': 'director',
        'cast': 'actors',
        'rating': 'imdb_rating',
        'movie_id': 'imdb_id'
    })

    bolly = bolly[['title','release_year','director','actors','imdb_rating','imdb_id']]

    return tmdb, bolly

def merge_file(tmdb, bolly):
    merged = pd.concat([tmdb, bolly], ignore_index=True)
    merged.drop_duplicates(subset=['title', 'release_year'], inplace=True)
    return merged
