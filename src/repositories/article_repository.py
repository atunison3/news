import json
import sqlite3
from typing import Iterable

from helper_functions import str_to_dt, dt_to_str
from models.article import Article


class ArticleRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def upsert(self, article: Article) -> None:
        self.conn.execute(
            """
            INSERT INTO articles (
                url,
                title,
                source,
                published_at,
                summary,
                read_time,
                content_type,
                image_url,
                tags,
                first_seen_at,
                last_seen_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ON CONFLICT(url)
            DO UPDATE SET
                title = excluded.title,
                source = excluded.source,
                published_at = excluded.published_at,
                summary = excluded.summary,
                read_time = excluded.read_time,
                content_type = excluded.content_type,
                image_url = excluded.image_url,
                tags = excluded.tags,
                last_seen_at = CURRENT_TIMESTAMP
            """,
            (
                str(article.url),
                article.title,
                article.source,
                dt_to_str(article.published_at),
                article.summary,
                article.read_time,
                article.content_type,
                str(article.image_url) if article.image_url else None,
                json.dumps(article.tags),
            ),
        )

    def upsert_many(self, articles: Iterable[Article]) -> None:
        for article in articles:
            self.upsert(article)

    def get_by_url(self, url: str) -> Article | None:
        row = self.conn.execute(
            """
            SELECT *
            FROM articles
            WHERE url = ?
            """,
            (url,),
        ).fetchone()

        return self._row_to_article(row) if row else None

    def list_all(self, limit: int = 100) -> list[Article]:
        rows = self.conn.execute(
            """
            SELECT *
            FROM articles
            ORDER BY published_at DESC, first_seen_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

        return [self._row_to_article(row) for row in rows]

    def _row_to_article(self, row: sqlite3.Row) -> Article:
        return Article(
            url=row["url"],
            title=row["title"],
            source=row["source"],
            published_at=str_to_dt(row["published_at"]),
            first_seen_at=str_to_dt(row["first_seen_at"]),
            last_seen_at=str_to_dt(row["last_seen_at"]),
            summary=row["summary"],
            read_time=row["read_time"],
            content_type=row["content_type"],
            image_url=row["image_url"],
            tags=json.loads(row["tags"]) if row["tags"] else [],
        )
