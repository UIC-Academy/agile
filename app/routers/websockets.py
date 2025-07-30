from fastapi import APIRouter, HTTPException, WebSocket

from app.dependencies import db_dep
from app.models import User
from app.utils import decode_user_from_jwt_token

router = APIRouter(
    prefix="/ws",
    tags=["WebSockets"],
)


@router.websocket("/")
async def websocket_endpoint(db: db_dep, websocket: WebSocket, token: str):
    user_email = decode_user_from_jwt_token(token=token).get("email")

    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"You are {user.email}! Message text was: {data}")
