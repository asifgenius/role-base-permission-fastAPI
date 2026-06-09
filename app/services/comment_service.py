from fastapi import status

from app.exceptions.custom_exception import AppException
from app.models.comment import Comment
from app.models.user import Role, User
from app.repositories.comment_repository import CommentRepository
from app.repositories.post_repository import PostRepository
from app.schemas.comment import CommentCreate
from app.services.authorization_service import AuthorizationService


class CommentService:
    @staticmethod
    def list_comments(post_id: int, user: User) -> list[Comment]:
        post = PostRepository.get_post(post_id)
        if not AuthorizationService.can_read(user):
            raise AppException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return CommentRepository.list_comments_for_post_by_author(post.id, user.id)

    @staticmethod
    def create_comment(post_id: int, payload: CommentCreate, user: User) -> Comment:
        post = PostRepository.get_post(post_id)
        if not AuthorizationService.can_create_comment(user, post):
            raise AppException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return CommentRepository.create_comment(post.id, user.id, payload.body)

    @staticmethod
    def delete_comment(post_id: int, comment_id: int, user: User) -> None:
        post = PostRepository.get_post(post_id)
        if user.role == Role.GUEST:
            raise AppException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

        if user.role == Role.REGULAR_USER and post.author_id != user.id:
            comment = CommentRepository.find_comment(comment_id)
            if comment is None or comment.post_id != post.id or comment.author_id != user.id:
                raise AppException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
            CommentRepository.delete_comment(comment.id)
            return

        comment = CommentRepository.get_comment(comment_id)
        if not AuthorizationService.can_delete_comment(user, post, comment):
            raise AppException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        CommentRepository.delete_comment(comment.id)

