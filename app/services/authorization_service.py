from app.models.comment import Comment
from app.models.post import Post
from app.models.user import Role, User


class AuthorizationService:
    @staticmethod
    def can_read(user: User) -> bool:
        return user.role in {
            Role.SUPER_ADMIN,
            Role.MODERATOR,
            Role.REGULAR_USER,
            Role.GUEST,
        }

    @staticmethod
    def can_manage_users(user: User) -> bool:
        return user.role == Role.SUPER_ADMIN

    @staticmethod
    def can_create_post(user: User) -> bool:
        return user.role == Role.REGULAR_USER

    @staticmethod
    def can_update_post(user: User, post: Post) -> bool:
        if user.role == Role.REGULAR_USER:
            return post.author_id == user.id
        return False

    @staticmethod
    def can_delete_post(user: User, post: Post) -> bool:
        if user.role in {Role.SUPER_ADMIN, Role.MODERATOR}:
            return True
        if user.role == Role.REGULAR_USER:
            return post.author_id == user.id
        return False

    @staticmethod
    def can_create_comment(user: User, post: Post) -> bool:
        del post
        return user.role == Role.REGULAR_USER

    @staticmethod
    def can_delete_comment(user: User, post: Post, comment: Comment) -> bool:
        if comment.post_id != post.id:
            return False
        if user.role in {Role.SUPER_ADMIN, Role.MODERATOR}:
            return True
        if user.role != Role.REGULAR_USER:
            return False
        return comment.author_id == user.id or post.author_id == user.id

