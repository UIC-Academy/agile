from datetime import UTC, datetime, timedelta

from fastapi import Request, Response
from jose import jwt
from sqlalchemy.orm import Session
from starlette_admin.auth import AuthProvider
from starlette_admin.exceptions import LoginFailed

from app.dependencies import get_db
from app.enums import RoleEnum
from app.models import User
from app.settings import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ADMIN_REMEMBER_ME_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
)
from app.utils import verify_password


class JSONAuthProvider(AuthProvider):
    async def login(
        self,
        email: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ):
        db: Session = next(get_db())
        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise LoginFailed("User not found.")

        if user and user.role != RoleEnum.admin:
            raise LoginFailed("User is not admin.")

        if not verify_password(password, user.password):
            raise LoginFailed("Invalid password.")

        if remember_me:
            access_token_expires = timedelta(minutes=ADMIN_REMEMBER_ME_EXPIRE_MINUTES)
        else:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        token_data = {
            "sub": user.email,
            "exp": datetime.now(UTC) + access_token_expires,
        }
        access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            secure=True,
            samesite="lax",
        )

        return response

    async def is_authenticated(self, request: Request) -> User | None:
        token = request.cookies.get("access_token")

        if not token:
            return None

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                return None

            db: Session = next(get_db())
            user = db.query(User).filter(User.email == email).first()

            if user is None or user.role != RoleEnum.admin:
                return None

            return user

        except jwt.JWTError:
            return None

    async def logout(self, request: Request, response: Response) -> Response:
        response.delete_cookie("access_token")
        return response
