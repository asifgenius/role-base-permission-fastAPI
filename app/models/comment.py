from dataclasses import dataclass


@dataclass(frozen=True)
class Comment:
    id: int
    post_id: int
    author_id: int
    body: str

