import sqlite3
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from domain.article import Article

DB_PATH = Path('/Users/andrewtunison/app_data/new_articles_dev.db')

class ArticleRepository:
    def __init__(self):
        self.db_path = DB_PATH

    def _get_connection(self) -> sqlite3.Connection:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON')
        return conn

    def get_by_id(self, article_id: int) -> Optional[Article]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM articles WHERE id = ?', (article_id,))
            row = cursor.fetchone()
            if row:
                published_at = datetime.fromisoformat(row['published_at']) if row['published_at'] else None
                return Article(
                    id=row['id'],
                    url=row['url'],
                    title=row['title'],
                    source=row['source'],
                    published_at=published_at,
                    has_opened=bool(row['has_opened']),
                    has_read=bool(row['has_read']),
                    thumbs_up=row['thumbs_up'] if row['thumbs_up'] is not None else None,
                    summary=row['summary'],
                    content_type=row['content_type'],
                    image_url=row['image_url'],
                    tags=row['tags']
                )
            return None

    def get_all(self) -> List[Article]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT *
                FROM articles
                ORDER BY
                    RANDOM() * CASE
                        WHEN has_read = 1 THEN 0.0001   -- 0.01%
                        WHEN has_opened = 1 THEN 0.01   -- 1%
                        ELSE 1.0                        -- 100%
                    END
                LIMIT 25;
                ''')
            rows = cursor.fetchall()
            articles = [
                Article(
                    id=row['id'],
                    url=row['url'],
                    title=row['title'],
                    source=row['source'],
                    published_at=datetime.fromisoformat(row['published_at']) if row['published_at'] else None,
                    summary=row['summary'],
                    content_type=row['content_type'],
                    image_url=row['image_url'],
                    has_opened=bool(row['has_opened']),
                    has_read=bool(row['has_read']),
                    thumbs_up=row['thumbs_up'] if row['thumbs_up'] is not None else None,
                    tags=row['tags']
                ) for row in rows
            ]

            return articles

    def mark_opened(self, article_id: int) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE articles SET has_opened = 1 WHERE id = ?',
                (article_id,)
            )

    def mark_read(self, article_id: int) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE articles SET has_read = 1 WHERE id = ?',
                (article_id,)
            )

    def vote(self, article_id: int, thumbs_up: bool) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE articles SET thumbs_up = ? WHERE id = ?',
                (thumbs_up, article_id)
            )

