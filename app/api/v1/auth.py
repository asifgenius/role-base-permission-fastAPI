from fastapi import APIRouter

from app.dependencies import public_route
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(tags=["auth"])


@router.post("/auth/login", response_model=TokenResponse)
@public_route
def login(payload: LoginRequest) -> TokenResponse:
    return AuthService.login(payload.email, payload.password)
