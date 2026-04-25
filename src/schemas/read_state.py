from pydantic import BaseModel

class ReadStateRequest(BaseModel):
    article_url: HttpUrl
    is_read: bool