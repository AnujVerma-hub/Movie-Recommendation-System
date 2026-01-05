import pandas as pd

from SRC.Orchestrator1 import MovieOrchestrator

movies_df = pd.read_csv("datasets/imdb_enriched.csv")

orch = MovieOrchestrator(movies_df)

