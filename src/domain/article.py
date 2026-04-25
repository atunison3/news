from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, HttpUrl, Field


class Article(BaseModel):
    url: HttpUrl
    title: str
    source: str

    published_at: Optional[datetime] = None

    first_seen_at: Optional[datetime] = None
    last_seen_at: Optional[datetime] = None

    summary: Optional[str] = None


class ArticleUserState(BaseModel):
    article_url: HttpUrl

    is_read: bool = False
    read_at: Optional[datetime] = None

    vote: Optional[Literal["up", "down"]] = None

    saved: bool = False
    archived: bool = False

    notes: Optional[str] = None


class ArticleView(BaseModel):
    url: HttpUrl
    title: str
    source: str
    published_at: Optional[datetime] = None
    summary: Optional[str] = None

    # user state
    is_read: bool = False
    vote: Optional[Literal["up", "down"]] = None
    saved: bool = False
    archived: bool = False


class VoteRequest(BaseModel):
    article_url: HttpUrl
    vote: Literal["up", "down"]


class ReadStateRequest(BaseModel):
    article_url: HttpUrl
    is_read: bool
