from app.core.security import create_access_token, decode_access_token, verify_password
from app.exceptions.custom_exception import AppException
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenResponse


class AuthService:
    @staticmethod
    def get_user(user_id: int) -> User:
        return UserRepository.get_user(user_id)

    @staticmethod
    def get_user_from_token(token: str) -> User:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise ValueError("Token is missing subject")
        return UserRepository.get_user(int(user_id))

    @staticmethod
    def login(email: str, password: str) -> TokenResponse:
        user = UserRepository.get_user_by_email(email)
        if not verify_password(password, user.password_hash):
            raise AppException(status_code=401, detail="Invalid credentials")
        token = create_access_token(subject=str(user.id), role=user.role.value)
        return TokenResponse(access_token=token)
