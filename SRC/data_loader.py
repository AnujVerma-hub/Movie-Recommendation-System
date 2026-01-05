import pandas as pd
import requests
import time
from tqdm import tqdm

def data_base_loader(path: str) -> pd.DataFrame:

    df = pd.read_csv(path)
    df.columns = df.columns.str.lower().str.strip()

    useful_col = ["title", "genre", "overview", "release_date", "id"]
    df = df[[col for col in useful_col if col in df.columns]]

    df.dropna(subset="title", inplace=True)
    df.drop_duplicates(subset="title", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def add_omdb_info(df: pd.DataFrame, api_key: str, limit: int=1000) -> pd.DataFrame:
    
    titles = df["title"].head(limit)
    movie_data = []

    for title in tqdm(titles):
        try:
            url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
            response = requests.get(url)
            data = response.json()
            if data.get('Response') == 'True':
                movie_data.append({
                    'title': data.get('Title'),
                    'imdb_rating': data.get('imdbRating'),
                    'runtime': data.get('Runtime'),
                    'director': data.get('Director'),
                    'actors': data.get('Actors'),
                    'plot_omdb': data.get('Plot'),
                    'Genre': data.get('Genre'),
                    'writer': data.get('Writer'),
                    'imdb_votes': data.get('imdbVotes'),
                    'released': data.get('Released'),
                    'language': data.get('Language'),
                    'country': data.get('Country'),
                    'production': data.get('Production'),
                    'poster': data.get('Poster')
                })

            time.sleep(0.3)
        except Exception as e:
            print(f"Erroe fetching {title}; {e}")

    omdb_df = pd.DataFrame(movie_data)
    merged_data = pd.merge(df, omdb_df,on='title',how='left')
    return merged_data


def merge_datasets(base_path: str, api_key: str) -> pd.DataFrame:
    df = data_base_loader(base_path)
    df = add_omdb_info(df, api_key)
    print("Final merged dataset ready")
    return df