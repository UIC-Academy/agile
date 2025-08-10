from enum import Enum


class RoleEnum(str, Enum):
    admin = "admin"
    developer = "developer"
    tester = "tester"
    manager = "manager"
    user = "user"


class StatusEnum(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    READY_FOR_TEST = "READY_FOR_TEST"
    DONE = "DONE"


class TaskPriorityEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class WSEventTypes(str, Enum):
    task_created = "task_created"
    task_status_change = "task_status_change"
    task_move_ready = "task_move_ready"
    task_rejected = "task_rejected"
    task_created_high = "task_created_high"
