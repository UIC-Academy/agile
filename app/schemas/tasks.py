from enum import Enum


class StatusEnum(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    READY_FOR_TEST = "READY_FOR_TEST"
    DONE = "DONE"
