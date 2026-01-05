from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from capabilities.movie_details import get_movie_details
from capabilities.recommend_item import recommend_similar
import pandas as pd 

movies_df = pd.read_csv("datasets/imdb_enriched.csv")

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/movie/{id}",response_class=HTMLResponse)
def movie_details(request: Request, id: int):
    movie = get_movie_details(id,movies_df)

    recommended = recommend_similar(
        movie_id=id,movies_df=movies_df,top_k=10
    )

    return templates.TemplateResponse(
        "movie_details.html",
        {
            "request": request,
            "movie": movie,
            "recommended":recommended
        }
    )