from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, HttpUrl, Field


class Article(BaseModel):
    url: HttpUrl
    title: str
    source: str
    published_at: datetime | None = None
    first_seen_at: datetime | None = None
    last_seen_at: datetime | None = None
    summary: str | None = None
    read_time: str | None = None
    content_type: str | None = None
    image_url: HttpUrl | None = None
    tags: list[str] = Field(default_factory=list)









