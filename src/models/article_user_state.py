from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, HttpUrl, Field


class ArticleUserState(BaseModel):
    article_url: HttpUrl
    has_read: bool = False
    has_opened: bool = False
    read_at: datetime | None = None
    vote: Literal['up', 'down'] | None = None
    saved: bool = False
    archived: bool = False
    notes: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None