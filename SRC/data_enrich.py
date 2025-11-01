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

        
 

