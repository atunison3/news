import sqlite3
from pathlib import Path
from repositories.article_repository import ArticleRepository
from repositories.article_user_state_repository import ArticleUserStateRepository
from repositories.article_view_repository import ArticleViewRepository

def get_connection(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')

    return conn


class NewsService:

    def __init__(self, db_path: Path):
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON')

        return conn
    
    def ingest(self, scraped_articles: list):
        with get_connection(self.db_path) as conn:
            article_repo = ArticleRepository(conn)
            article_repo.upsert_many(scraped_articles)

    def vote(self, article_url: str, vote: str):
        with get_connection(self.db_path) as conn:
            state_repo = ArticleUserStateRepository(conn)
            state_repo.set_vote(article_url, vote)

    def get_feed(self, limit: int = 50):
        with get_connection(self.db_path) as conn:
            view_repo = ArticleViewRepository(conn)
            return view_repo.list_feed(limit=limit)
        

    def mark_as_read(self, article_url: str) -> None:
        with get_connection(self.db_path) as conn:
            state_repo = ArticleUserStateRepository(conn)
            state_repo.mark_opened(article_url)
            state_repo.mark_read(article_url)

    def mark_as_opened(self, article_url: str) -> None:
        with get_connection(self.db_path) as conn:
            state_repo = ArticleUserStateRepository(conn)
            state_repo.mark_opened(article_url)