from typing import Protocol, Iterable, Optional
from datetime import datetime

from models import Article, ArticleUserState


class ArticleRepository(Protocol):
    def upsert_articles(self, articles: Iterable[Article]) -> None: ...

    def get_articles(
        self,
        limit: int = 100,
        unread_only: bool = False,
    ) -> list[Article]: ...

    def get_recent_articles(
        self,
        since: datetime,
    ) -> list[Article]: ...


class ArticleUserStateRepository(Protocol):
    def get_state(self, article_url: str) -> Optional[ArticleUserState]: ...

    def get_all_states(self) -> dict[str, ArticleUserState]: ...

    def mark_read(self, article_url: str) -> None: ...

    def set_vote(self, article_url: str, vote: str) -> None: ...

    def set_saved(self, article_url: str, saved: bool) -> None: ...

    def set_archived(self, article_url: str, archived: bool) -> None: ...
