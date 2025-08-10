from datetime import datetime

from pydantic import BaseModel

from app.enums import StatusEnum, TaskPriorityEnum


class TaskListProjectNested(BaseModel):
    key: str


class TaskListUserNested(BaseModel):
    id: int
    email: str
    fullname: str | None


class TaskListResponse(BaseModel):
    id: int
    project: TaskListProjectNested
    key: str
    summary: str
    status: StatusEnum
    priority: str


class TaskDetailResponse(BaseModel):
    id: int
    project: TaskListProjectNested
    key: str
    summary: str
    description: str | None
    status: StatusEnum
    priority: str
    assignee: TaskListUserNested
    reporter: TaskListUserNested
    due_date: datetime


class TaskCreateRequest(BaseModel):
    project_id: int
    summary: str
    description: str | None
    status: StatusEnum
    priority: TaskPriorityEnum
    assignee_id: int
    reporter_id: int
    due_date: str


class TaskUpdateRequest(BaseModel):
    summary: str | None
    description: str | None
    priority: TaskPriorityEnum | None
    assignee_id: int | None
    reporter_id: int | None
    due_date: str | None


class TaskMoveRequest(BaseModel):
    status: StatusEnum
