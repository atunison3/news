import sqlite3
from numpy.random import shuffle
from pathlib import Path
from repositories.article_repository import ArticleRepository

def get_connection(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


class NewsService:

    def __init__(self, db_path: Path):
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")

        return conn

    def get_feed(self, limit: int = 25):
        article_repo = ArticleRepository()

        articles = article_repo.get_all()
        articles.sort(key = lambda a: a.published_at, reverse=True)

        return articles

    def mark_as_opened(self, article_id: int) -> None:
        article_repo = ArticleRepository()
        article_repo.mark_opened(article_id)

    def mark_as_read(self, article_id: int) -> None:
        article_repo = ArticleRepository()
        article_repo.mark_read(article_id)
