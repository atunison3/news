from pydantic import BaseModel, HttpUrl


class ReadStateRequest(BaseModel):
    article_url: HttpUrl
    has_read: bool
