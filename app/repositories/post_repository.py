from fastapi import status

from app.database.connection import SessionLocal
from app.database.entities import PostEntity
from app.exceptions.custom_exception import AppException
from app.models.post import Post


class PostRepository:
    @staticmethod
    def list_posts() -> list[Post]:
        with SessionLocal() as session:
            rows = session.query(PostEntity).order_by(PostEntity.id).all()
            return [Post(id=row.id, author_id=row.author_id, title=row.title, body=row.body) for row in rows]

    @staticmethod
    def get_post(post_id: int) -> Post:
        with SessionLocal() as session:
            row = session.get(PostEntity, post_id)
            if row is None:
                raise AppException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
            return Post(id=row.id, author_id=row.author_id, title=row.title, body=row.body)

    @staticmethod
    def create_post(author_id: int, title: str, body: str) -> Post:
        with SessionLocal() as session:
            row = PostEntity(author_id=author_id, title=title, body=body)
            session.add(row)
            session.commit()
            session.refresh(row)
            return Post(id=row.id, author_id=row.author_id, title=row.title, body=row.body)

    @staticmethod
    def update_post(post: Post, title: str, body: str) -> Post:
        with SessionLocal() as session:
            row = session.get(PostEntity, post.id)
            if row is None:
                raise AppException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
            row.title = title
            row.body = body
            session.commit()
            return Post(id=row.id, author_id=row.author_id, title=row.title, body=row.body)

    @staticmethod
    def delete_post(post_id: int) -> None:
        with SessionLocal() as session:
            row = session.get(PostEntity, post_id)
            if row is None:
                raise AppException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
            session.delete(row)
            session.commit()
