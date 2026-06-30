from datetime import datetime, timedelta, UTC
from fastapi import HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.security.jwt import create_access_token, create_refresh_token, hash_refresh_token, decode_token
from app.security.password import hash_password, verify_password


class AuthService:

    def __init__(self, db: AsyncSession):
        self.db=db

    async def signup(self, data):

        existing = await self.db.scalar(
            select(User).where(User.email == data.email)
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )
        
        user = User(
            name=data.name,
            email=data.email,
            password=hash_password(data.password),
        )

        self.db.add(user)

        await self.db.flush()

        access_token = create_access_token(user.id)

        refresh_token, jti = create_refresh_token(user.id)

        refresh = RefreshToken(
            user_id=user.id,
            jti=jti,
            token_hash=hash_refresh_token(refresh_token),
            expires_at=datetime.now(UTC) + timedelta(days=7),
        )

        self.db.add(refresh)
        await self.db.commit()

        await self.db.refresh(user)

        return (
            user,
            access_token,
            refresh_token,
        )


    
    async def login(self, data):

        user = await self.db.scalar(
            select(User).where(User.email == data.email)
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if not verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        #remove previous refresh tokens
        await self.db.execute(
            delete(RefreshToken).where(
                RefreshToken.user_id == user.id
            )
        )

        access_token = create_access_token(user.id)

        refresh_token, jti = create_refresh_token(user.id)

        refresh = RefreshToken(
            user_id=user.id,
            jti=jti,
            token_hash=hash_refresh_token(refresh_token),
            expires_at=datetime.now(UTC) + timedelta(days=7),
        )

        self.db.add(refresh)

        await self.db.commit()

        return user, access_token, refresh_token
    

    async def refresh(self, refresh_token: str):

        payload = decode_token(refresh_token)

        if payload["type"] != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        token_hash = hash_refresh_token(refresh_token)

        db_token = await self.db.scalar(
            select(RefreshToken).where(
                RefreshToken.token_hash == token_hash,
                RefreshToken.revoked == False,
            )
        )

        if not db_token:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Refresh token not found"
                )

        user = await self.db.get(
            User,
            db_token.user_id,
    )

        if not user:
            raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found"
                    )
        

        # delete old refresh token
        await self.db.execute(
            delete(RefreshToken).where(
                RefreshToken.user_id == user.id
            )
        )

        access_token = create_access_token(user.id)

        new_refresh_token, jti = create_refresh_token(user.id)

        refresh = RefreshToken(
            user_id=user.id,
            jti=jti,
            token_hash=hash_refresh_token(
                new_refresh_token
            ),
            expires_at=datetime.now(UTC)
            + timedelta(days=7),
        )

        self.db.add(refresh)

        await self.db.commit()

        return (
            access_token,
            new_refresh_token,
        )