<<<<<<< HEAD
import pandas as pd
import requests
import time
import urllib.parse
import os

API_KEY = "b7e4526c"

INPUT_PATH = "datasets/merged_clean_movies_2.csv"

OUTPUT_PATH = "datasets/enriched_movies.csv"

batch_size = 800
sleep_between_calls = 1.2

def load_master():

    if os.path.exists(OUTPUT_PATH):
        df = pd.read_csv(OUTPUT_PATH,low_memory=False)

    else:
        df = pd.read_csv(INPUT_PATH, low_memory=False)

    return df

def fetch_data(title):
    if not isinstance(title, str) or title.strip() == "":
        return None
    q = urllib.parse.quote(title)
    url = f"http://www.omdbapi.com/?t={q}&apikey={API_KEY}"

    try:
        r = requests.get(url)
        data = r.json()
        if data.get("Response") == "True":
            return {
                "imdb_id": data.get("imdbID"),
                "imdb_rating": data.get("imdbRating"),
                'genre': data.get('Genre'),
                'actors': data.get('Actors'),
                'poster': data.get('Poster'),
                'director': data.get('Director'),
                'language': data.get('Language')
            }
        
    except Exception as e:
        print(f"Request error for {title}: {e}")

    return None


def enrich_with_omdb(df, batch_size=batch_size):
    needs = df[df["imdb_rating"].isna() | df["imdb_rating"].eq("") | df["imdb_rating"].isnull()]
    if len(needs) == 0:
        return df
    


    to_process = needs.head(batch_size).copy()
    updates = {}

    for idx, row in to_process.iterrows():
        title = row.get('title') or row.get('movie_title')
        if not isinstance(title, str) or title.strip() == "":
            continue

        info = fetch_data(title.strip())

        if info:
            updates[idx] = info

        else:
            print(" no data from omdb")

        time.sleep(sleep_between_calls)

    for idx, info in updates.items():
        for col, val in info.items():
            df.loc[idx, col] = val

    return df
    

def main():
    df = load_master()
    for c in ["imdb_rating", 'genre', 'actors', 'poster', 'director', 'language','imdb_id']:
        if c  not in df.columns:
            df[c] = pd.NA

    df_updated = enrich_with_omdb(df, batch_size)


    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)


    df_updated.to_csv(OUTPUT_PATH, index=False)
    print("File saved successsfully")


main()






        
 

=======
import pandas as pd
import requests
import time
import urllib.parse

API_KEY = "b7e4526c"

INPUT_PATH = "datasets/merged_clean_movies.csv"

OUTPUT_PATH = "datasets/enriched_movies.csv"

def enrich_with_omdb(df: pd.DataFrame, api_key: str, limit: int= 1000) -> pd.DataFrame:
    

    if limit:
        df = df.head(limit)

    if 'title' not in df.columns:
        raise KeyError("The Datasets must have a 'title' column")
    

    required_cols = ['imdb_rating', 'genre', 'actors', 'poster', 'director', 'language']
    for col in required_cols:
        if col not in df.columns:
            df[col] = None


    for index,row in df.iterrows():
        title = str(row['title']).strip()

        if pd.notnull(row.get('imdb_rating')) and row.get("imdb_rating") != "":
         continue

        url = f"http://www.omdbapi.com/?t={urllib.parse.quote(title)}&apikey={api_key}"

        try:
            response = requests.get(url)
            data = response.json()

            if data.get("Response") == "True":
                df.loc[index,"imdb_rating"] = data.get("imdbRating"),
                df.loc[index,"genre"] = data.get("Genre")
                df.loc[index,"actors"] = data.get("Actors")
                df.loc[index,"poster"] = data.get("Poster")
                df.loc[index,"director"] = data.get("Director")
                df.loc[index,"language"] = data.get("Language")
                print(f"Updated: {title}")
            else:
                print(f"skipped: {title} - {data.get('Error')}")

            time.sleep(0.3)

        except Exception as e:
            print(f"Error fetching {title}: {e}")


df = pd.read_csv(INPUT_PATH)

enriched_df = enrich_with_omdb(df, API_KEY)

enriched_df.to_csv(OUTPUT_PATH,index=False)

print(f"Enriched datsets saved successfully")

        
 

>>>>>>> c3c6ca92a336cd6574d1aaff61eb205b609d0812
