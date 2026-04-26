from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, HttpUrl, Field

class ArticleView(BaseModel):
    url: HttpUrl
    title: str
    source: str
    published_at: datetime | None = None
    summary: str | None = None
    read_time: str | None = None
    content_type: str | None = None
    image_url: HttpUrl | None = None
    tags: list[str] = Field(default_factory=list)

    has_read: bool = False
    has_opened: bool = False
    read_at: datetime | None = None
    opened_at: datetime | None = None
    vote: Literal['up', 'down'] | None = None
    saved: bool = False
    archived: bool = False
    notes: str | None = None