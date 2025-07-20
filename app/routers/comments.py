from fastapi import APIRouter

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/{task_key}/comments/")
async def get_task_comments():
    pass


@router.get("/comments/{comment_id}/")
async def detail_comment():
    pass


@router.post("/comments/create/")
async def write_comment():
    pass


@router.put("/comments/{comment_id}/update/")
async def update_comment():
    pass


@router.delete("/comments/{comment_id}/delete/")
async def delete_comment():
    pass
