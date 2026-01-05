import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import time 
import random
import re

DATA_PATH = "datasets/top_20k_movies.csv"

SAVE_PATH = "datasets/imdb_enriched.csv"

BATCH_SIZE = 500

SLEEP_TIME = 2


ott_keywords = {
            "Netflix": ["netflix"],
            'Amazon Prime Video': ['primevideo','amazon'],
            'Disney+ hotstar': ['disney', 'hotstar', 'Jiohotstar'],
            'Zee5': ['zee5'],
            'Youtube': ['youtube', 'googleplay'],
            'Apple TV+': ['apple'],
            'Mx Player': ['mxplayer'],
        }


def load_progress():
    try:
        return pd.read_csv(SAVE_PATH)
    except:
        return pd.DataFrame()
    

def fetch_imdb(imdb_id):
    url = f"https://www.imdb.com/title/{imdb_id}/"
    headers = { "User-Agent": "Mozilla/5.0"}


    try:
        response = requests.get(url, headers=headers,timeout=10)

        if response.status_code != 200:
            print("IMDB page not found")
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(" ").lower()

        found = [name for name, keys in ott_keywords.items() if any(k in text for k in keys)]
        if found:
            print(f"found providers for {imdb_id}: {','.join(found)}")

            return found
        else:
            print(f"No providers found")
            return None

    except Exception as e:
        print(f"error fetching imdb page: {e}")
        return None
    




def get_imdb_rating(imdb_id):
    if imdb_id is None:
        return None
    
    url = f"https://www.imdb.com/title/{imdb_id}/"

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers,timeout=10)

        if r.status_code != 200:
            print("Rating error:", r.status_code)
            return None
        
    except:
        return None
    
    soup = BeautifulSoup(r.text, "html.parser")

    text = soup.get_text(" ", strip=True)

    match = re.search(r"(\d\.\d)\s*/\s*10", text)
    if match:
        return match.group(1)
    
    return None



def scrape_batch():
    full_df = pd.read_csv(DATA_PATH)
    scraped_df = load_progress()


    REQUIRED_COLS = ["imdb_id", "imdb_rating", "where_to_watch"]

    #for col in REQUIRED_COLS:
        #scraped_df[col] = None


    





    if scraped_df.empty:
        scraped_df = full_df.iloc[0:0].copy()
        scraped_df["imdb_rating"] = []
        scraped_df["where_to_watch"] = []
        

    pending = full_df[~full_df["imdb_id"].isin(scraped_df["imdb_id"])]

    if pending.empty:
        print("All movies scraped already")
        return
        
    batch = pending.head(BATCH_SIZE)

    new_rows = []

    print(f"Scraping batch of {len(batch)} movies...")

    for _,row in tqdm(batch.iterrows(), total=len(batch)):
        imdb_id = row["imdb_id"]

        platforms = fetch_imdb(imdb_id)
        rating = get_imdb_rating(imdb_id)

        row_data = row.to_dict()
        row_data["imdb_rating"] = rating
        row_data["where_to_watch"] =platforms

        new_rows.append(row_data)

        time.sleep(SLEEP_TIME)


    new_df = pd.DataFrame(new_rows)


    updated = pd.concat([scraped_df, new_df], ignore_index=True)


    updated.to_csv(SAVE_PATH, index=False)



    print(f"Saved batch -> {SAVE_PATH}")
    print(f"Remaining: {len(pending) - BATCH_SIZE}")




if __name__ =="__main__":
    scrape_batch()

