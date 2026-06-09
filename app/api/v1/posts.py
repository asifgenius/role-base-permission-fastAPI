from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies import allow_roles, current_user
from app.models.user import Role, User
from app.schemas.post import PostCreate, PostUpdate
from app.services.post_service import PostService

router = APIRouter(tags=["posts"])


@router.get("/posts")
@allow_roles(Role.SUPER_ADMIN, Role.MODERATOR, Role.REGULAR_USER, Role.GUEST)
def list_posts(user: Annotated[User, Depends(current_user)]):
    return PostService.list_posts(user)


@router.get("/posts/{post_id}")
@allow_roles(Role.SUPER_ADMIN, Role.MODERATOR, Role.REGULAR_USER, Role.GUEST)
def read_post(post_id: int, user: Annotated[User, Depends(current_user)]):
    return PostService.read_post(post_id, user)


@router.post("/posts", status_code=status.HTTP_201_CREATED)
@allow_roles(Role.REGULAR_USER)
def create_post(payload: PostCreate, user: Annotated[User, Depends(current_user)]):
    return PostService.create_post(payload, user)


@router.put("/posts/{post_id}")
@allow_roles(Role.REGULAR_USER)
def update_post(
    post_id: int,
    payload: PostUpdate,
    user: Annotated[User, Depends(current_user)],
):
    return PostService.update_post(post_id, payload, user)


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
@allow_roles(Role.SUPER_ADMIN, Role.MODERATOR, Role.REGULAR_USER)
def delete_post(post_id: int, user: Annotated[User, Depends(current_user)]) -> None:
    PostService.delete_post(post_id, user)
