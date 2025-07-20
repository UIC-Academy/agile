from fastapi import APIRouter

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/notifications/")
async def get_notifications():
    """User's notifications List"""
    pass


@router.get("/notifications/{notification_id}/")
async def read_notification():
    pass
