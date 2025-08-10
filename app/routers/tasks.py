from fastapi import APIRouter, HTTPException, Request, Response

from app.dependencies import (
    admin_user_dep,
    current_user_dep,
    db_dep,
    task_creatable_user_dep,
)
from app.enums import StatusEnum, TaskPriorityEnum, WSEventTypes
from app.models import Project, Task
from app.schemas import (
    TaskCreateRequest,
    TaskDetailResponse,
    TaskListResponse,
    TaskMoveRequest,
    TaskUpdateRequest,
)
from app.services import generate_task_key
from app.websocket.manager import dispatch_ws_event

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/all/", response_model=list[TaskListResponse])
async def get_tasks(admin_user: admin_user_dep, db: db_dep):
    """Admin only"""
    tasks = db.query(Task).all()

    return tasks


@router.get("/{task_key}/")
async def get_task_by_key(current_user: current_user_dep, db: db_dep, task_key: str):
    task = db.query(Task).filter(Task.key == task_key).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.post("/create/", response_model=TaskDetailResponse)
async def create_task(
    current_user: task_creatable_user_dep,
    db: db_dep,
    data: TaskCreateRequest,
    request: Request,
):
    project = db.query(Project).filter(Project.id == data.project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    task = Task(
        project_id=data.project_id,
        summary=data.summary,
        description=data.description,
        key=generate_task_key(db=db, project=project),
        status=data.status,
        priority=data.priority,
        reporter_id=current_user.id,
        assignee_id=data.assignee_id,
        due_date=data.due_date,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    ws_manager = request.app.state.ws_manager
    event_type = (
        WSEventTypes.task_created_high
        if data.priority == TaskPriorityEnum.HIGH
        else WSEventTypes.task_created
    )

    await dispatch_ws_event(
        ws_manager=ws_manager,
        event_type=event_type,
        project_id=task.project_id,
        payload={
            "type": event_type,
            "task_id": task.id,
            "project_id": task.project_id,
        },
    )

    return task


@router.put("/{task_id}/update/", response_model=TaskDetailResponse)
async def update_task(
    current_user: task_creatable_user_dep,
    db: db_dep,
    task_id: int,
    data: TaskUpdateRequest,
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.reporter_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You don't have permission to update this task"
        )

    for attr, value in data:
        setattr(task, attr, value)

    db.commit()
    db.refresh(task)

    return task


@router.patch("/{task_id}/move/", response_model=TaskDetailResponse)
async def move_task(
    current_user: current_user_dep, db: db_dep, task_id: int, move_data: TaskMoveRequest
):
    task = db.query(Task).filter(Task.id == task_id).first()
    old_status = task.status
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = move_data.status

    db.commit()
    db.refresh(task)

    # notify managers anyway, if task status changes
    ws_manager = current_user.app.state.ws_manager
    await dispatch_ws_event(
        ws_manager=ws_manager,
        event_type=WSEventTypes.task_status_change,
        project_id=task.project_id,
        payload={
            "type": WSEventTypes.task_status_change,
            "task_id": task.id,
            "project_id": task.project_id,
        },
    )

    # notify testers if the task is ready for test
    if task.status == StatusEnum.READY_FOR_TEST:
        ws_manager = current_user.app.state.ws_manager
        await dispatch_ws_event(
            ws_manager=ws_manager,
            event_type=WSEventTypes.task_move_ready,
            project_id=task.project_id,
            payload={
                "type": WSEventTypes.task_move_ready,
                "task_id": task.id,
                "project_id": task.project_id,
            },
        )

    # notify developers if the task is rejected
    if old_status == StatusEnum.READY_FOR_TEST and task.status == StatusEnum.TODO:
        await dispatch_ws_event(
            ws_manager=ws_manager,
            event_type=WSEventTypes.task_rejected,
            project_id=task.project_id,
            payload={
                "type": WSEventTypes.task_rejected,
                "task_id": task.id,
                "project_id": task.project_id,
            },
        )

    return task


@router.delete("/{task_id}/delete/")
async def delete_task(current_user: task_creatable_user_dep, db: db_dep, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.reporter_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You don't have permission to delete this task"
        )

    db.delete(task)
    db.commit()

    return Response(status_code=204)


@router.get("/{task_key}/comments/")
async def get_task_comments(current_user: current_user_dep, db: db_dep, task_key: str):
    task = db.query(Task).filter(Task.key == task_key).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    comments = task.comments.all()

    return comments
