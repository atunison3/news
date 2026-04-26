from pydantic import BaseModel, HttpUrl
from typing import Literal


class VoteRequest(BaseModel):
    article_url: HttpUrl
    vote: Literal["up", "down"]
