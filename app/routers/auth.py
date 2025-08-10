from fastapi import APIRouter, HTTPException

from app.celery import send_email
from app.dependencies import db_dep, oauth2_form_dep
from app.enums import RoleEnum
from app.models import User
from app.schemas import TokenResponse, UserRegisterRequest
from app.settings import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    FRONTEND_URL,
    REFRESH_TOKEN_EXPIRE_MINUTES,
)
from app.utils import (
    create_jwt_token,
    decode_user_from_jwt_token,
    generate_confirmation_token,
    hash_password,
    verify_password,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register/")
async def register_user(db: db_dep, register_data: UserRegisterRequest):
    is_user_exists = db.query(User).filter(User.email == register_data.email).first()

    if is_user_exists:
        raise HTTPException(status_code=400, detail="User already exists")

    is_first_user = db.query(User).count() == 0

    if is_first_user:
        user = User(
            email=register_data.email,
            password=hash_password(register_data.password),
            role=RoleEnum.admin,
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return {"detail": f"Admin user created with email: {user.email}"}
    else:
        user = User(
            email=register_data.email,
            password=hash_password(register_data.password),
            role=RoleEnum.user,
            is_active=False,  # not confirmed yet
            is_deleted=False,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # send confirmation email
        token = generate_confirmation_token(user_id=user.id)

        send_email.delay(
            to_email=user.email,
            subject="Confirm your registration to Agile",
            body=f"You can click the link to confirm your email: {FRONTEND_URL}/auth/confirm/{token}/",
        )

        return {
            "detail": f"Confirmation email sent to {user.email}. Please confirm to finalize your registration.",
        }


@router.post("/login/")
async def login(form_data: oauth2_form_dep, db: db_dep):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_jwt_token(
        {"user_id": user.id, "role": user.role},
        expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    refresh_token = create_jwt_token(
        {"user_id": user.id, "role": user.role},
        expires_delta=REFRESH_TOKEN_EXPIRE_MINUTES,
    )

    return TokenResponse(
        access_token=access_token, refresh_token=refresh_token, token_type="Bearer"
    )


@router.get("/confirm/{token}/")
async def confirm_email(db: db_dep, token: str):
    print("Confirming email...", token)
    user_id = decode_user_from_jwt_token(token=token).get("user_id")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    user.is_active = True
    db.commit()
    db.refresh(user)

    return {"detail": "Email confirmed"}
