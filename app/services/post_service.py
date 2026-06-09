from fastapi import status

from app.exceptions.custom_exception import AppException
from app.models.post import Post
from app.models.user import User
from app.repositories.comment_repository import CommentRepository
from app.repositories.post_repository import PostRepository
from app.schemas.post import PostCreate, PostUpdate
from app.services.authorization_service import AuthorizationService


class PostService:
    @staticmethod
    def list_posts(user: User) -> list[Post]:
        if not AuthorizationService.can_read(user):
            raise AppException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return PostRepository.list_posts()

    @staticmethod
    def read_post(post_id: int, user: User) -> Post:
        if not AuthorizationService.can_read(user):
            raise AppException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return PostRepository.get_post(post_id)

    @staticmethod
    def create_post(payload: PostCreate, user: User) -> Post:
        if not AuthorizationService.can_create_post(user):
            raise AppException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return PostRepository.create_post(user.id, payload.title, payload.body)

    @staticmethod
    def update_post(post_id: int, payload: PostUpdate, user: User) -> Post:
        post = PostRepository.get_post(post_id)
        if not AuthorizationService.can_update_post(user, post):
            raise AppException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return PostRepository.update_post(post, payload.title, payload.body)

    @staticmethod
    def delete_post(post_id: int, user: User) -> None:
        post = PostRepository.get_post(post_id)
        if not AuthorizationService.can_delete_post(user, post):
            raise AppException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        PostRepository.delete_post(post_id)
        CommentRepository.delete_comments_for_post(post_id)

