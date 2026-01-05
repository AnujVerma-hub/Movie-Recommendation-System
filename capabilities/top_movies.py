import pandas as pd
from typing import List,Dict
def fetch_movies(movies_df:pd.DataFrame,limit:int =12,sort_col:str | None= None,ascending=False,genre:str|None = None,columns:list[str] | None = None) -> List[Dict]:
    df = movies_df.copy()
    if genre:
        df = df[df["genres"].str.contains(genre,case=False,na=False)]


    if sort_col:
        if sort_col not in df.columns:
            raise ValueError(f"Column '{sort_col}' not found in dataframe")
        

        df = df.sort_values(by=sort_col,ascending=ascending)

    if columns:
        df = df.loc[:,columns]


    df = df.head(limit)

    return df.to_dict(orient="records")



        



    



