from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/users/{id}/")
async def get_user_by_id(id: int):
    pass


@router.get("/profile/")
async def get_profile():
    pass


@router.put("/profile/update/")
async def update_profile():
    pass


@router.post("/avatar/upload/")
async def upload_avatar():
    pass


@router.delete("/profile/delete/")
async def delete_profile():
    pass
