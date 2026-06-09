from fastapi import status

from app.database.connection import SessionLocal
from app.database.entities import CommentEntity
from app.exceptions.custom_exception import AppException
from app.models.comment import Comment


class CommentRepository:
    @staticmethod
    def list_comments_for_post_by_author(post_id: int, author_id: int) -> list[Comment]:
        with SessionLocal() as session:
            rows = (
                session.query(CommentEntity)
                .filter(CommentEntity.post_id == post_id, CommentEntity.author_id == author_id)
                .order_by(CommentEntity.id)
                .all()
            )
            return [
                Comment(id=row.id, post_id=row.post_id, author_id=row.author_id, body=row.body)
                for row in rows
            ]

    @staticmethod
    def find_comment(comment_id: int) -> Comment | None:
        with SessionLocal() as session:
            row = session.get(CommentEntity, comment_id)
            if row is None:
                return None
            return Comment(id=row.id, post_id=row.post_id, author_id=row.author_id, body=row.body)

    @staticmethod
    def get_comment(comment_id: int) -> Comment:
        with SessionLocal() as session:
            row = session.get(CommentEntity, comment_id)
            if row is None:
                raise AppException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
            return Comment(id=row.id, post_id=row.post_id, author_id=row.author_id, body=row.body)

    @staticmethod
    def create_comment(post_id: int, author_id: int, body: str) -> Comment:
        with SessionLocal() as session:
            row = CommentEntity(post_id=post_id, author_id=author_id, body=body)
            session.add(row)
            session.commit()
            session.refresh(row)
            return Comment(id=row.id, post_id=row.post_id, author_id=row.author_id, body=row.body)

    @staticmethod
    def delete_comment(comment_id: int) -> None:
        with SessionLocal() as session:
            row = session.get(CommentEntity, comment_id)
            if row is None:
                raise AppException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
            session.delete(row)
            session.commit()

    @staticmethod
    def delete_comments_for_post(post_id: int) -> None:
        with SessionLocal() as session:
            session.query(CommentEntity).filter(CommentEntity.post_id == post_id).delete()
            session.commit()
