from sqlalchemy import select

from app.database.connection import SessionLocal, engine
from app.database.entities import Base, CommentEntity, PostEntity, UserEntity
from seed import seed_state


def init_database() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        has_users = session.scalar(select(UserEntity.id).limit(1)) is not None
        if not has_users:
            _seed_database(session)


def reset_state() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        _seed_database(session)


def _seed_database(session) -> None:
    seeded_state = seed_state()

    for user in seeded_state["users"].values():
        session.add(
            UserEntity(
                id=user.id,
                role=user.role,
                email=user.email,
                password_hash=user.password_hash,
            )
        )

    for post in seeded_state["posts"].values():
        session.add(
            PostEntity(
                id=post.id,
                author_id=post.author_id,
                title=post.title,
                body=post.body,
            )
        )

    for comment in seeded_state["comments"].values():
        session.add(
            CommentEntity(
                id=comment.id,
                post_id=comment.post_id,
                author_id=comment.author_id,
                body=comment.body,
            )
        )

    session.commit()
