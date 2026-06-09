from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.models.user import Role


class Base(DeclarativeBase):
    pass


class UserEntity(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    posts: Mapped[list["PostEntity"]] = relationship(back_populates="author")
    comments: Mapped[list["CommentEntity"]] = relationship(back_populates="author")


class PostEntity(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=False)

    author: Mapped[UserEntity] = relationship(back_populates="posts")
    comments: Mapped[list["CommentEntity"]] = relationship(
        back_populates="post",
        cascade="all, delete-orphan",
    )


class CommentEntity(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=False)

    post: Mapped[PostEntity] = relationship(back_populates="comments")
    author: Mapped[UserEntity] = relationship(back_populates="comments")
