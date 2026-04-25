from datetime import date

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from numpy.random import shuffle

import helper_functions as fun

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")
app.mount('/static', StaticFiles(directory='src/static'), name='static')

@app.get('/')
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context={
            'page_title': 'Home',
        },
    )

@app.get('/news')
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
