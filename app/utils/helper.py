from fastapi import Cookie, HTTPException, status

async def get_refresh_token(
    refresh_token: str | None = Cookie(default=None),
) -> str:
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
        )
    return refresh_token