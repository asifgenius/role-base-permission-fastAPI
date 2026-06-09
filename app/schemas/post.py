from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    body: str


class PostUpdate(BaseModel):
    title: str
    body: str

