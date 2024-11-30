from enum import Enum


class JobStatus(Enum):
    NEW = 1
    PROCESSING = 2
    COMPLETED = 3
    FAILED = 4


class JobType(Enum):
    CREATE = 1
    EDIT = 2


class Job:
    def __init__(self, id: str, type: JobType, args: str, status: JobStatus) -> None:
        self._id = id
        self._type = type
        self._status = status
        self._args = args

    @property
    def id(self) -> str:
        return self._id

    @property
    def type(self) -> JobType:
        return self._type

    @property
    def args(self) -> str:
        return self._args

    @property
    def status(self) -> JobStatus:
        return self._status

    def __str__(self) -> str:
        return f"Job(id={self._id}, type={self._type.name}, args={self._args}, status={self._status.name})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__
