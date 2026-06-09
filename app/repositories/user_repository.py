from fastapi import status

from app.database.connection import SessionLocal
from app.database.entities import UserEntity
from app.exceptions.custom_exception import AppException
from app.models.user import User


class UserRepository:
    @staticmethod
    def get_user(user_id: int) -> User:
        with SessionLocal() as session:
            user = session.get(UserEntity, user_id)
            if user is None:
                raise AppException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown user")
            return User(
                id=user.id,
                role=user.role,
                email=user.email,
                password_hash=user.password_hash,
            )

    @staticmethod
    def get_user_by_email(email: str) -> User:
        with SessionLocal() as session:
            user = session.query(UserEntity).filter(UserEntity.email == email).one_or_none()
            if user is None:
                raise AppException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
            return User(
                id=user.id,
                role=user.role,
                email=user.email,
                password_hash=user.password_hash,
            )
