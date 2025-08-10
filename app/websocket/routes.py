from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select

from app.dependencies import get_db
from app.enums import RoleEnum
from app.models import Project, ProjectMember, User
from app.websocket.dependencies import ws_current_user_dep

router = APIRouter(
    prefix="/ws",
    tags=["WebSockets"],
)


@router.websocket("/connect")
async def websocket_endpoint(websocket: WebSocket, user_data: ws_current_user_dep):
    user_id = user_data["user_id"]
    role = RoleEnum(user_data["role"])
    # projects = user_data["projects"]

    # === MANUAL DB SESSION (SYNC) ===
    db = next(get_db())
    try:
        user = db.query(User).filter(User.id == user_id).first()
        projects = (
            db.execute(
                select(Project.id)
                .select_from(Project)
                .join(Project.members)  # assuming project_members is the relationship
                .where(ProjectMember.user_id == user.id)
            )
            .scalars()
            .all()
        )
    finally:
        db.close()

    ws_manager = websocket.app.state.ws_manager

    await ws_manager.connect(
        user_id=user_id, role=role, projects=projects, websocket=websocket
    )

    try:
        await websocket.send_json(
            {
                "type": "connected",
                "user_id": user_id,
                "role": role,
                "projects": projects,
            }
        )
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await ws_manager.disconnect(user_id)
