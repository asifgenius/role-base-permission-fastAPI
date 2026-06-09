from typing import Annotated

from fastapi import Header, Request, status

from app.exceptions.custom_exception import AppException
from app.models.user import Role, User
from app.services.auth_service import AuthService


def current_user(
    request: Request,
    authorization: Annotated[str | None, Header(alias="Authorization")] = None,
) -> User:
    if authorization is None:
        raise AppException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
        )
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise AppException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth scheme")
    user = AuthService.get_user_from_token(token)
    _enforce_endpoint_roles(request, user)
    return user


def allow_roles(*allowed_roles: Role):
    def decorator(func):
        setattr(func, "__allowed_roles__", allowed_roles)
        return func

    return decorator


def public_route(func):
    setattr(func, "__public_route__", True)
    return func


def _enforce_endpoint_roles(request: Request, user: User) -> None:
    endpoint = request.scope.get("endpoint")
    if endpoint is None:
        return

    allowed_roles = getattr(endpoint, "__allowed_roles__", None)
    if allowed_roles is None:
        return

    if user.role not in allowed_roles:
        raise AppException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
