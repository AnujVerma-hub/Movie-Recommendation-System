from justwatch import JustWatch
import os
import pandas as pd
import time 

COUNTRY = "IN"
INPUT_PATH = "datasets/enriched_movies.csv"
OUTPUT_PATH = "datasets/movies_with_provider.csv"
BATCH_SIZE = 100
SLEPP_BETWEEN_CALLS = 1.0

def get_watch_providers(title, country=COUNTRY):
    try:
        justwatch = JustWatch(country=country)
        results = justwatch.search_for_item(query=title)
        if not results["items"]:
            return None
        
        offers = results["items"][0].get("offers", [])
        providers = list({offer["provider_id"] for offer in offers if "provider_id" in offers})
        provider_dict = {
            8: "Netflix", 9: "Amazon Prime Video", 337: "Jiocinema",
            119: "Zee5", 384: "Apple TV+", 11: "Hotstar",
            98: "Mx Player", 350: "SonyLiv", 386: "Youtube"
        }

        provider_names = [provider_dict.get(pid, f"provider_{pid}") for pid in providers]
        return ",".join(provider_names) if provider_names else None
    
    except Exception as e:
        print(f"Error fetching {title}: {e}")
        return None
    

def enrich_with_providers(df, batch_size=BATCH_SIZE):
    needs = df[df["available_on"].isnull()]
    print(f"found {len(needs)} movies without provider info")

    to_process = needs.head(batch_size).copy()
    for idx, row in to_process.iterrows():
        title = row.get("title")
        if not isinstance(title, str) or not title.strip():
            continue


        print(f"fetching watch providers for: {title}")
        providers = get_watch_providers(title)
        if providers:
            df.loc[idx, "available_on"] = providers
            print(f"{providers}")

        else:
            print(f"No providers found")

        time.sleep(SLEPP_BETWEEN_CALLS)

    return df

def main():
    if not os.path.exists(INPUT_PATH):
        print(f"input_file not found")

        return
    
    df = pd.read_csv(INPUT_PATH)
    if "available_on" not in df.columns:
        df["available_on"] = pd.NA

    df = enrich_with_providers(df)
    df.to_csv(OUTPUT_PATH,index=False)
    print(f"Saved updated dataset")

main()
    

