from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
from pydantic import BaseModel

from authorization import Authorization, Comment, Post, Role, User

app = FastAPI(title="Posts API", version="1.0.0")


class PostCreate(BaseModel):
    title: str
    body: str


class PostUpdate(BaseModel):
    title: str
    body: str


class CommentCreate(BaseModel):
    body: str


users = {
    1: User(id=1, role=Role.SUPER_ADMIN),
    2: User(id=2, role=Role.MODERATOR),
    3: User(id=3, role=Role.REGULAR_USER),
    4: User(id=4, role=Role.REGULAR_USER),
    5: User(id=5, role=Role.REGULAR_USER),
    6: User(id=6, role=Role.GUEST),
}
posts: dict[int, Post] = {}
comments: dict[int, Comment] = {}
next_post_id = 1
next_comment_id = 1


def get_user(user_id: int) -> User:
    user = users.get(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown user")
    return user


def get_post(post_id: int) -> Post:
    post = posts.get(post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


def get_comment(comment_id: int) -> Comment:
    comment = comments.get(comment_id)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment


def current_user(
    query_user_id: Annotated[int | None, Query(alias="user_id")] = None,
    user_id: Annotated[int | None, Header(alias="User-Id")] = None,
) -> User:
    resolved_user_id = query_user_id
    if resolved_user_id is None:
        resolved_user_id = user_id
    if resolved_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Missing user_id query parameter or User-Id header",
        )
    return get_user(resolved_user_id)


@app.get("/posts")
def list_posts(user: Annotated[User, Depends(current_user)]) -> list[Post]:
    if not Authorization.can_read(user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return list(posts.values())


@app.get("/posts/{post_id}")
def read_post(post_id: int, user: Annotated[User, Depends(current_user)]) -> Post:
    if not Authorization.can_read(user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return get_post(post_id)


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate, user: Annotated[User, Depends(current_user)]) -> Post:
    if not Authorization.can_create_post(user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    global next_post_id
    post = Post(id=next_post_id, author_id=user.id, title=payload.title, body=payload.body)
    posts[post.id] = post
    next_post_id += 1
    return post


@app.put("/posts/{post_id}")
def update_post(
    post_id: int,
    payload: PostUpdate,
    user: Annotated[User, Depends(current_user)],
) -> Post:
    post = get_post(post_id)
    if not Authorization.can_update_post(user, post):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    updated = Post(id=post.id, author_id=post.author_id, title=payload.title, body=payload.body)
    posts[post.id] = updated
    return updated


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, user: Annotated[User, Depends(current_user)]) -> None:
    post = get_post(post_id)
    if not Authorization.can_delete_post(user, post):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    posts.pop(post_id)
    for comment_id, comment in list(comments.items()):
        if comment.post_id == post_id:
            comments.pop(comment_id)


@app.post("/posts/{post_id}/comments", status_code=status.HTTP_201_CREATED)
def create_comment(
    post_id: int,
    payload: CommentCreate,
    user: Annotated[User, Depends(current_user)],
) -> Comment:
    post = get_post(post_id)
    if not Authorization.can_create_comment(user, post):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    global next_comment_id
    comment = Comment(
        id=next_comment_id,
        post_id=post.id,
        author_id=user.id,
        body=payload.body,
    )
    comments[comment.id] = comment
    next_comment_id += 1
    return comment


@app.get("/posts/{post_id}/comments")
def list_comments(post_id: int, user: Annotated[User, Depends(current_user)]) -> list[Comment]:
    post = get_post(post_id)
    if not Authorization.can_read(user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return [comment for comment in comments.values() if comment.post_id == post.id]


@app.delete("/posts/{post_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    post_id: int,
    comment_id: int,
    user: Annotated[User, Depends(current_user)],
) -> None:
    post = get_post(post_id)
    comment = get_comment(comment_id)
    if not Authorization.can_delete_comment(user, post, comment):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    comments.pop(comment.id)
