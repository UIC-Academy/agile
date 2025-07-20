from fastapi import APIRouter

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/projects/all/")
async def get_all_projects():
    """Admin only"""
    pass


@router.get("/projects/joined/")
async def get_joined_projects():
    """List of projects user has joined"""
    pass


@router.get("/projects/{project_key}/")
async def get_project_by_id(project_id: int):
    pass


@router.post("/projects/create/")
async def create_project():
    pass


@router.put("/projects/{project_key}/update/")
async def update_project():
    pass


@router.post("/projects/{project_key}/deactivate/")
async def deactivate_project():
    pass


@router.post("/projects/{project_key}/delete")
async def delete_project():
    pass


### Members


@router.get("/projects/{project_key}/members/")
async def get_project_members():
    pass


@router.post("/projects/{project_key}/members/invite/")
async def invite_project_member():
    pass


@router.post("/projects/{project_key}/members/kick/")
async def kick_project_member():
    pass
