from fastapi import APIRouter, Depends, Response, Request ,HTTPException, status
from app.schemas.auth import LoginRequest, SignupRequest
from app.models.user import User
from app.services.auth_service import AuthService
from app.core.auth_dependencies import get_auth_service, get_current_user
from app.utils.helper import get_refresh_token

router = APIRouter()

@router.post("/signup")
async def signup(
    request: SignupRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service)    
):
    user, access_token, refresh_token = await service.signup(request)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=900,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=604800,
    )

    return {
        "message": "Signup successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    }

@router.post("/login")
async def login(
    request: LoginRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    
    user, access_token, refresh_token = await service.login(request)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=900,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=604800,
    )

    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }


@router.post("/refresh")
async def refresh(
    response: Response,
    refresh_token: str = Depends(get_refresh_token),
    service: AuthService = Depends(get_auth_service),
):
    
    access_token, refresh_token = await service.refresh(
        refresh_token
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=900,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=604800,
    )

    return {
        "message": "Token refreshed"
    }


@router.get("/me")
async def me(
    current_user: User = Depends(
        get_current_user
    ),
):

    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
    }