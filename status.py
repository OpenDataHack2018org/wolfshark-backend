from enum import Enum


class Status(Enum):
    QUEUED = 1
    PROCESSING = 2
    COMPLETED = 3
    ERROR = 4
