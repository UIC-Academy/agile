from fastapi import APIRouter

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/tasks/all/")
async def get_tasks():
    """Admin only"""
    pass


@router.get("/tasks/{task_key}/")
async def get_task_by_key():
    pass


@router.get("/{project_key}/tasks/")
async def get_project_tasks():
    pass
