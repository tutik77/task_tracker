from pydantic import BaseModel

from src.utils.structs import Status


class TaskSchemaAdd(BaseModel):
    title: str
    description: str | None = None
    status: Status


class TaskSchemaUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Status | None = None
