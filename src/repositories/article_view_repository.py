from datetime import datetime, timezone
import json
import sqlite3
from typing import Iterable

from helper_functions import *
from models.article_view import ArticleView

class ArticleViewRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def list_feed(
        self,
        source: str | None = None,
        unread_only: bool = False,
        saved_only: bool = False,
        include_archived: bool = False,
        limit: int = 100,
    ) -> list[ArticleView]:

        where_clauses = []
        params = []

        if source:
            where_clauses.append('a.source = ?')
            params.append(source)

        if unread_only:
            where_clauses.append('COALESCE(s.is_read, 0) = 0')

        if saved_only:
            where_clauses.append('COALESCE(s.saved, 0) = 1')

        if not include_archived:
            where_clauses.append('COALESCE(s.archived, 0) = 0')

        where_sql = ''
        if where_clauses:
            where_sql = 'WHERE ' + ' AND '.join(where_clauses)

        params.append(limit)

        rows = self.conn.execute(
            f'''
            SELECT
                a.url,
                a.title,
                a.source,
                a.published_at,
                a.summary,
                a.read_time,
                a.content_type,
                a.image_url,
                a.tags,

                COALESCE(s.is_read, 0) AS is_read,
                s.read_at,
                s.vote,
                COALESCE(s.saved, 0) AS saved,
                COALESCE(s.archived, 0) AS archived,
                s.notes

            FROM articles a
            LEFT JOIN article_user_state s
                ON a.url = s.article_url

            {where_sql}

            ORDER BY
                COALESCE(s.is_read, 0) ASC,
                a.published_at DESC,
                a.first_seen_at DESC

            LIMIT ?
            ''',
            params,
        ).fetchall()

        return [self._row_to_view(row) for row in rows]

    def _row_to_view(self, row: sqlite3.Row) -> ArticleView:
        return ArticleView(
            url=row['url'],
            title=row['title'],
            source=row['source'],
            published_at=str_to_dt(row['published_at']),
            summary=row['summary'],
            read_time=row['read_time'],
            content_type=row['content_type'],
            image_url=row['image_url'],
            tags=json.loads(row['tags']) if row['tags'] else [],
            is_read=bool(row['is_read']),
            read_at=str_to_dt(row['read_at']),
            vote=row['vote'],
            saved=bool(row['saved']),
            archived=bool(row['archived']),
            notes=row['notes'],
        )