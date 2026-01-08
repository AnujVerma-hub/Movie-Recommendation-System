from fastapi import FastAPI, Request, Query,Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
import uvicorn
from main import router
import os
from capabilities.top_movies import fetch_movies
from capabilities.search import search_movie
from typing import Optional
from pydantic import BaseModel
from SRC.movie_mapper import MovieMapper

from SRC.Orchestrator1 import MovieOrchestrator

class ChatRequest(BaseModel):
    message:str

class ChatResponse(BaseModel):
    answer:str


app = FastAPI(title="Movie Recommendation System")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


app.include_router(router)
_movies_df = None
_orch = None
_mapper = None

def get_movies_df():
    global _movies_df
    if _movies_df is None:
        _movies_df = pd.read_csv("datasets/imdb_enriched.csv")

    return _movies_df

def get_mapper():
    global _mapper
    if _mapper is None:
        _mapper = MovieMapper("datasets/imdb_enriched.csv")

    return _mapper


def get_orchestrator():
    global _orch

    if _orch is None:
        movies_df = get_movies_df()
        _orch =MovieOrchestrator(movies_df)
    return _orch


@app.get("/search",response_class=HTMLResponse)
def search_movie(request: Request,q:Optional[str]= None):
    if not q or q.strip() == "":
        movies = []
    else:
        orch = get_orchestrator()
        movies = orch.search(q)

    return templates.TemplateResponse(
        "index.html",
        {
            "request":request,
            "movies": movies,
            "query":q or ""
        }
    )




@app.get("/",response_class=HTMLResponse)
def home(request: Request):
    """
    Home page :show top movies amd search option
    """
    movies_df = get_movies_df()

    top_movies = fetch_movies(
            movies_df,
            sort_col="imdb_rating",
            limit=12,
            columns=["id","title","poster_path","imdb_rating","genres"]
    )

    action_movies = fetch_movies(
        movies_df,
        genre="Action",
        sort_col="imdb_rating",
        limit=12,
        columns=["id","title","poster_path"]
    )


    comedy_movies = fetch_movies(
        movies_df,
        genre="comedy",
        limit=12,
        columns=["id","title","poster_path"]   
    )


    drama_movies = fetch_movies(
        movies_df,
        genre="Drama",
        limit=12,
        columns=["id","title","poster_path"]
    )

    return templates.TemplateResponse(
        "index.html",
        {
            "request":request,
            "top_movies":top_movies,
            "action_movies":action_movies,
            "comedy_movies":comedy_movies,
            "drama_movies":drama_movies
        }

    )
    

@app.get("/global_chat",response_class=HTMLResponse)
def global_chat_page(request:Request):
    return templates.TemplateResponse(
        "global_chat.html",
        {
            "request":request
        }
    )

@app.post("/chat/global",response_model=ChatResponse)
def global_chat_api( chat:ChatRequest):
    user_message = chat.message
    orch = get_orchestrator()
    mapper = get_mapper()

    answer = orch.chat(user_message)
    return {"answer":answer}

@app.get("/movie/{id}/chat",response_class=HTMLResponse)
@app.post("/movie/{id}/chat",response_class=HTMLResponse)
async def movie_chat_page(request:Request,id:int):
    orch = get_orchestrator()
    mapper = get_mapper()
    movie = mapper.get_movie_by_id(id)

    response = None

    if request.method == "POST":
        form = await request.form()
        user_message = form.get("message")

        response = orch.chat(
            message=user_message,
            movie_id=id
        )

    return templates.TemplateResponse(
        "movie_chat.html",
        {
            "request":request,
            "movie":movie,
            "response":response,
            "movie_id":id
        }
    )




    