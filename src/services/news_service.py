import sqlite3
from repositories.article_repository import ArticleRepository
from repositories.article_user_state_repository import ArticleUserStateRepository
from repositories.article_view_repository import ArticleViewRepository

def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')

    return conn


class NewsService:

    def ingest(self, scraped_articles):
        with get_connection() as conn:
            article_repo = ArticleRepository(conn)
            article_repo.upsert_many(scraped_articles)

    def vote(self, article_url: str, vote: str):
        with get_connection() as conn:
            state_repo = ArticleUserStateRepository(conn)
            state_repo.set_vote(article_url, vote)

    def get_feed(self, limit: int = 50):
        with get_connection() as conn:
            view_repo = ArticleViewRepository(conn)
            return view_repo.list_feed(limit=limit)