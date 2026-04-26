from datetime import datetime, timezone
import sqlite3

from models.article_user_state import ArticleUserState

class ArticleUserStateRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def get_by_url(self, article_url: str) -> ArticleUserState | None:
        row = self.conn.execute(
            '''
            SELECT *
            FROM article_user_state
            WHERE article_url = ?
            ''',
            (article_url,),
        ).fetchone()

        return self._row_to_state(row) if row else None

    def get_all_by_url(self) -> dict[str, ArticleUserState]:
        rows = self.conn.execute(
            '''
            SELECT *
            FROM article_user_state
            '''
        ).fetchall()

        return {
            row['article_url']: self._row_to_state(row)
            for row in rows
        }

    def mark_read(self, article_url: str) -> None:
        read_at = datetime.now(timezone.utc).isoformat() if True else None

        self.conn.execute(
            '''
            INSERT INTO article_user_state (
                article_url,
                has_read,
                read_at
            )
            VALUES (?, ?, ?)
            ON CONFLICT(article_url)
            DO UPDATE SET
                has_read = excluded.has_read,
                read_at = excluded.read_at,
                updated_at = CURRENT_TIMESTAMP
            ''',
            (article_url, int(True), read_at),
        )

    def mark_opened(self, article_url: str) -> None:
        '''Updates the article to having been opened'''

        opened_at = datetime.now(timezone.utc).isoformat() if True else None

        self.conn.execute(
            '''
            INSERT INTO article_user_state (
                article_url,
                has_opened,
                opened_at
            )
            VALUES (?, ?, ?)
            ON CONFLICT(article_url)
            DO UPDATE SET
                has_opened = excluded.has_opened,
                opened_at = excluded.opened_at,
                updated_at = CURRENT_TIMESTAMP
            ''',
            (article_url, int(True), opened_at),
        )

    def set_vote(self, article_url: str, vote: str | None) -> None:
        self.conn.execute(
            '''
            INSERT INTO article_user_state (
                article_url,
                vote
            )
            VALUES (?, ?)
            ON CONFLICT(article_url)
            DO UPDATE SET
                vote = excluded.vote,
                updated_at = CURRENT_TIMESTAMP
            ''',
            (article_url, vote),
        )

    def set_saved(self, article_url: str, saved: bool) -> None:
        self.conn.execute(
            '''
            INSERT INTO article_user_state (
                article_url,
                saved
            )
            VALUES (?, ?)
            ON CONFLICT(article_url)
            DO UPDATE SET
                saved = excluded.saved,
                updated_at = CURRENT_TIMESTAMP
            ''',
            (article_url, int(saved)),
        )

    def set_archived(self, article_url: str, archived: bool) -> None:
        self.conn.execute(
            '''
            INSERT INTO article_user_state (
                article_url,
                archived
            )
            VALUES (?, ?)
            ON CONFLICT(article_url)
            DO UPDATE SET
                archived = excluded.archived,
                updated_at = CURRENT_TIMESTAMP
            ''',
            (article_url, int(archived)),
        )

    def set_notes(self, article_url: str, notes: str | None) -> None:
        self.conn.execute(
            '''
            INSERT INTO article_user_state (
                article_url,
                notes
            )
            VALUES (?, ?)
            ON CONFLICT(article_url)
            DO UPDATE SET
                notes = excluded.notes,
                updated_at = CURRENT_TIMESTAMP
            ''',
            (article_url, notes),
        )

    def _row_to_state(self, row: sqlite3.Row) -> ArticleUserState:
        return ArticleUserState(
            article_url=row['article_url'],
            has_read=bool(row['has_read']),
            has_opened=bool(row['has_opened']),
            read_at=str_to_dt(row['read_at']),
            opened_at=str_to_dt(row['opened_at']),
            vote=row['vote'],
            saved=bool(row['saved']),
            archived=bool(row['archived']),
            notes=row['notes'],
            created_at=str_to_dt(row['created_at']),
            updated_at=str_to_dt(row['updated_at']),
        )