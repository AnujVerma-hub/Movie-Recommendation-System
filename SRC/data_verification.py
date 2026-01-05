<<<<<<< HEAD
import pandas as pd
path = "datasets/merged_movies.csv"
save_path = "datasets/cleaned_data.csv"

def verify_and_cleaned(path: str, save_path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print("Before cleaning", df.shape)

    df.drop_duplicates(subset='title', inplace=True)
    df.dropna(subset=['title'], inplace=True)

    df['imdb_rating'] = pd.to_numeric(df['imdb_rating'], errors='coerce')
    #df['genre'] = df['genre'].fillna("").apply(lambda x: x.lower().replace(",", " "))
    print("After cleaning", df.shape)

    return df

=======
import pandas as pd
path = "datasets/merged_movies.csv"
save_path = "datasets/cleaned_data.csv"

def verify_and_cleaned(path: str, save_path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print("Before cleaning", df.shape)

    df.drop_duplicates(subset='title', inplace=True)
    df.dropna(subset=['title'], inplace=True)

    df['imdb_rating'] = pd.to_numeric(df['imdb_rating'], errors='coerce')
    #df['genre'] = df['genre'].fillna("").apply(lambda x: x.lower().replace(",", " "))
    print("After cleaning", df.shape)

    return df

>>>>>>> c3c6ca92a336cd6574d1aaff61eb205b609d0812
