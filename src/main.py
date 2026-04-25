import sqlite3

from datetime import date
from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from numpy.random import shuffle
from pathlib import Path

from services.news_service import NewsService
from scrapers.white_house import get_white_house_news
from scrapers.nasa import get_nasa_news

router = APIRouter()
templates = Jinja2Templates(directory='templates')

service = NewsService()

ENV = 'dev'
DB_PATH = Path(f'src/data/news_{ENV}_.db')

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")
app.mount('/static', StaticFiles(directory='src/static'), name='static')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(schema_path: Path):
    '''Initiates the database'''

    with get_connection() as conn:
        with open(schema_path, 'r') as f:
            conn.executescript(f.read())


@app.on_event('startup')
def startup():
    schema_path = Path('src/database.sql')
    init_db(schema_path)


def get_votes_by_url():
    with get_connection() as conn:
        rows = conn.execute(
            'SELECT article_url, vote FROM article_votes'
        ).fetchall()

    return {row['article_url']: row['vote'] for row in rows}


# @app.post('/vote')
# def vote_article(
#     article_url: str = Form(...),
#     title: str = Form(...),
#     source: str = Form(...),
#     article_date: str = Form(''),
#     vote: str = Form(...),
# ):
#     with get_connection() as conn:
#         conn.execute(
#             '''
#             INSERT INTO article_votes (
#                 article_url,
#                 title,
#                 source,
#                 article_date,
#                 vote
#             )
#             VALUES (?, ?, ?, ?, ?)
#             ON CONFLICT(article_url)
#             DO UPDATE SET
#                 vote = excluded.vote,
#                 updated_at = CURRENT_TIMESTAMP
#             '''
#             ,
#             (
#                 article_url,
#                 title,
#                 source,
#                 article_date,
#                 vote,
#             ),
#         )

#     return RedirectResponse('/news', status_code=303)

@app.get('/')
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context={
            'page_title': 'Home',
        },
    )

@router.get('/news')
def news(request: Request):
    # scrape
    articles = []
    articles.extend(get_white_house_news())
    articles.extend(get_nasa_news())

    # persist
    service.ingest(articles)

    # query
    feed = service.get_feed()

    return templates.TemplateResponse(
        'news.html',
        {
            'request': request,
            'articles': feed,
        },
    )
