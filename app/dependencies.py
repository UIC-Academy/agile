from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.settings import ALGORITHM, SECRET_KEY


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dep = Annotated[Session, Depends(get_db)]

##### Authentication dependencies #####

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

oauth2_scheme_dep = Annotated[str, Depends(oauth2_scheme)]
oauth2_form_dep = Annotated[OAuth2PasswordRequestForm, Depends()]


async def get_current_user(db: db_dep, token: oauth2_scheme_dep):
    try:
        payload = jwt.decode(
            token=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": True},
        )

        email: str = payload.get("email")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError as err:
        raise HTTPException(status_code=401, detail="Invalid refresh token") from err
    except jwt.ExpiredSignatureError as err:
        raise HTTPException(
            status_code=401, detail="Refresh token has expired"
        ) from err


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


current_user_dep = Annotated[User, Depends(get_current_user)]
current_active_user_dep = Annotated[User, Depends(get_current_active_user)]
