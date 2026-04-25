from pydantic import BaseModel 

class VoteRequest(BaseModel):
    article_url: HttpUrl
    vote: Literal["up", "down"]


