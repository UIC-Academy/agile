import logging
from typing import Annotated, Any

from fastapi import Depends, WebSocket, status
from fastapi.exceptions import WebSocketException
from jose import JWTError, jwt

from app.settings import ALGORITHM, SECRET_KEY

logger = logging.getLogger(__name__)


async def get_current_user_ws(websocket: WebSocket) -> dict[str, Any]:
    """
    Extract and verify JWT from WebSocket query params. Returns payload.
    Raises WebSocketException if invalid.
    """
    token = websocket.query_params.get("token")

    if not token:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION, reason="Missing token"
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        role = payload.get("role")

        return {"user_id": user_id, "role": role}

    except (JWTError, ValueError) as e:
        logger.warning(f"JWT decode failed: {e}")

        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token"
        ) from e


ws_current_user_dep = Annotated[dict[str, Any], Depends(get_current_user_ws)]
