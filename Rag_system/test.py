import pandas as pd

from SRC.Orchestrator1 import MovieOrchestrator
from capabilities.recommend_user import recommend_user

movies_df = pd.read_csv("datasets/imdb_enriched.csv")

orch = MovieOrchestrator(movies_df)
#print("\n == SEARCH RESULTS ==")

#results = orch.search("dark", limit=5)


#for r in results:
    #print(
       # r.get("id"),
       # r["title"],
       # r.get("imdb_rating")
    #)


#print("\n === GLOBAL CHAT ===")
#response = orch.chat("Recommend some good thriller movies")
#print(response)


top_movies = orch.home(limit=10)

print(top_movies)















