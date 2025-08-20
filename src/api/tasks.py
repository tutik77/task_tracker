from typing import Annotated
import uuid
from fastapi import APIRouter, Depends

from src.schemas.tasks import TaskSchemaAdd, TaskSchemaUpdate
from src.services.tasks import TasksService
from src.dependencies.tasks import get_tasks_service
from src.utils.structs import Status

router = APIRouter()


@router.get("/")
async def get_tasks(
    service: Annotated[TasksService, Depends(get_tasks_service)],
    status: Status | None = None,
):
    return await service.get_tasks(status=status)


@router.post("/")
async def create_task(
    task: TaskSchemaAdd,
    service: Annotated[TasksService, Depends(get_tasks_service)],
):
    return await service.create_task(task)


@router.patch("/{task_id}")
async def update_task(
    task_id: uuid.UUID,
    task: TaskSchemaUpdate,
    service: Annotated[TasksService, Depends(get_tasks_service)],
):
    return await service.update_task(task_id, task)


@router.delete("/{task_id}")
async def delete_task(
    task_id: uuid.UUID,
    service: Annotated[TasksService, Depends(get_tasks_service)],
):
    return await service.delete_task(task_id)
