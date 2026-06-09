from app.models.comment import Comment
from app.models.post import Post
from app.models.user import Role, User
from app.core.security import hash_password


SEEDED_USERS = {
    1: User(
        id=1,
        role=Role.SUPER_ADMIN,
        email="admin@example.com",
        password_hash=hash_password("admin123"),
    ),
    2: User(
        id=2,
        role=Role.MODERATOR,
        email="moderator@example.com",
        password_hash=hash_password("moderator123"),
    ),
    3: User(
        id=3,
        role=Role.REGULAR_USER,
        email="usera@example.com",
        password_hash=hash_password("usera123"),
    ),
    4: User(
        id=4,
        role=Role.REGULAR_USER,
        email="userb@example.com",
        password_hash=hash_password("userb123"),
    ),
    5: User(
        id=5,
        role=Role.REGULAR_USER,
        email="userc@example.com",
        password_hash=hash_password("userc123"),
    ),
    6: User(
        id=6,
        role=Role.GUEST,
        email="guest@example.com",
        password_hash=hash_password("guest123"),
    ),
}

SEEDED_POSTS = {
    1: Post(id=1, author_id=3, title="First post", body="Hello world"),
}

SEEDED_COMMENTS: dict[int, Comment] = {}


def seed_users() -> dict[int, User]:
    return dict(SEEDED_USERS)


def seed_posts() -> dict[int, Post]:
    return dict(SEEDED_POSTS)


def seed_comments() -> dict[int, Comment]:
    return dict(SEEDED_COMMENTS)


def seed_state() -> dict[str, object]:
    posts = seed_posts()
    comments = seed_comments()
    return {
        "users": seed_users(),
        "posts": posts,
        "comments": comments,
        "next_post_id": max(posts.keys(), default=0) + 1,
        "next_comment_id": max(comments.keys(), default=0) + 1,
    }


if __name__ == "__main__":
    from app.database.base import reset_state

    reset_state()
    state = seed_state()
    print("Seeded users:")
    for user in state["users"].values():
        print(f"{user.id} -> {user.role.value} | {user.email}")
    print("Dummy passwords:")
    print("admin@example.com -> admin123")
    print("moderator@example.com -> moderator123")
    print("usera@example.com -> usera123")
    print("userb@example.com -> userb123")
    print("userc@example.com -> userc123")
    print("guest@example.com -> guest123")
    print(f"Posts: {len(state['posts'])}")
    print(f"Comments: {len(state['comments'])}")
