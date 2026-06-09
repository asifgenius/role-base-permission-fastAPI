from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies import allow_roles, current_user
from app.models.user import Role, User
from app.schemas.comment import CommentCreate
from app.services.comment_service import CommentService

router = APIRouter(tags=["comments"])


@router.get("/posts/{post_id}/comments")
@allow_roles(Role.SUPER_ADMIN, Role.MODERATOR, Role.REGULAR_USER, Role.GUEST)
def list_comments(post_id: int, user: Annotated[User, Depends(current_user)]):
    return CommentService.list_comments(post_id, user)


@router.post("/posts/{post_id}/comments", status_code=status.HTTP_201_CREATED)
@allow_roles(Role.REGULAR_USER)
def create_comment(
    post_id: int,
    payload: CommentCreate,
    user: Annotated[User, Depends(current_user)],
):
    return CommentService.create_comment(post_id, payload, user)


@router.delete("/posts/{post_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
@allow_roles(Role.SUPER_ADMIN, Role.MODERATOR, Role.REGULAR_USER)
def delete_comment(
    post_id: int,
    comment_id: int,
    user: Annotated[User, Depends(current_user)],
) -> None:
    CommentService.delete_comment(post_id, comment_id, user)
