from enum import Enum

from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class UserRegisterRequest(BaseModel):
    email: str
    password: str


class RoleEnum(str, Enum):
    admin = "admin"
    developer = "developer"
    tester = "tester"
    manager = "manager"
    user = "user"
