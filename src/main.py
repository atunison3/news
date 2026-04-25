import sqlite3

from datetime import date
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from numpy.random import shuffle
from pathlib import Path

import helper_functions as fun

ENV = "dev"
TABLE_NAME = f"article_votes_{ENV}"
DB_PATH = Path("news.db")

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")
app.mount("/static", StaticFiles(directory="src/static"), name="static")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS article_votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_url TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL,
                source TEXT NOT NULL,
                article_date TEXT,
                vote TEXT NOT NULL CHECK (vote IN ('up', 'down')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """)


@app.on_event("startup")
def startup():
    init_db()


def get_votes_by_url():
    with get_connection() as conn:
        rows = conn.execute("SELECT article_url, vote FROM article_votes").fetchall()

    return {row["article_url"]: row["vote"] for row in rows}


@app.post("/vote")
def vote_article(
    article_url: str = Form(...),
    title: str = Form(...),
    source: str = Form(...),
    article_date: str = Form(""),
    vote: str = Form(...),
):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO article_votes (
                article_url,
                title,
                source,
                article_date,
                vote
            )
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(article_url)
            DO UPDATE SET
                vote = excluded.vote,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                article_url,
                title,
                source,
                article_date,
                vote,
            ),
        )

    return RedirectResponse("/news", status_code=303)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "page_title": "Home",
        },
    )


@app.get("/news")
def index(request: Request):

    # Collect new articles from different sites
    articles = []
    articles += fun.get_white_house_news()
    articles += fun.get_nasa_news()

    # Shuffle news articles
    shuffle(articles)

    return templates.TemplateResponse(
        request=request,
        name="news.html",
        context={
            "today": date.today().strftime("%B %d, %Y"),
            "articles": articles,
        },
    )
