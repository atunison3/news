import logging
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

from helper_functions import setup_logger

logger = setup_logger('news_app')
logger.info('Starting news app.')

ENV = 'dev'
DB_PATH = Path(f'src/data/news_{ENV}_.db')

service = NewsService(DB_PATH)

app = FastAPI()
router = APIRouter()

templates = Jinja2Templates(directory="src/templates")
app.mount('/static', StaticFiles(directory='src/static'), name='static')


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')

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




@app.get('/')
def home(request: Request):
    logger.info('/Home')
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context={
            'page_title': 'Home',
        },
    )

@router.get('/news')
def news(request: Request):

    logger.info('Scraping news')

    # scrape
    articles = []
    try:
        articles.extend(get_white_house_news())
        logger.info('Successfully scraped white house news')
    except Exception as e:
        logger.error('Failed to scrape white house news')
    # try:
    #     articles.extend(get_nasa_news())
    #     logger.info('Successfully scraped NASA news')
    # except Exception as e:
    #     logger.error('Failed to scrape NASA news')   
    

    # persist
    service.ingest(articles)

    # query
    feed = service.get_feed()

    return templates.TemplateResponse(
        request=request,
        name='news.html',
        context={
            'page_title': 'News',
            'articles': feed,
            'today': date.today().strftime('%B %d, %Y'),
        },
    )

    
app.include_router(router)
for route in app.routes:
    logger.info(f'ROUTE: {route.path} | {route.name}')