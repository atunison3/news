import sqlite3

from datetime import date
from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from numpy.random import shuffle
from pathlib import Path

from services.news_service import NewsService

from helper_functions import setup_logger, should_filter_article

logger = setup_logger('news_app')
logger.info('Starting news app.')

DB_PATH = Path('/Users/andrewtunison/app_data/new_articles_dev.db')

service = NewsService(DB_PATH)

app = FastAPI()
router = APIRouter()

templates = Jinja2Templates(directory="src/templates")
app.mount('/static', StaticFiles(directory='src/static'), name='static')


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

    logger.info('Loading news feed')

    # query
    feed = service.get_feed(limit=25)

    return templates.TemplateResponse(
        request=request,
        name='news.html',
        context={
            'page_title': 'News',
            'articles': feed,
            'today': date.today().strftime('%B %d, %Y'),
        },
    )


@router.post('/articles/{article_id}/open')
def mark_article_opened(article_id: int):
    logger.info(f'Mark article opened | id={article_id}')
    try:
        service.mark_as_opened(article_id)
    except Exception as e:
        logger.exception('Failed to mark article opened')

    return {'status': 'ok'}


@router.post('/articles/{article_id}/read')
def mark_article_read(article_id: int):
    logger.info(f'Mark article read | id={article_id}')
    try:
        service.mark_as_read(article_id)
    except Exception as e:
        logger.exception('Failed to mark article read')

    return {'status': 'ok'}

app.include_router(router)
for route in app.routes:
    logger.info(f'ROUTE: {route.path} | {route.name}')