from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.schemas.tasks import TaskSchemaAdd, TaskSchemaUpdate
from src.utils.repository import AbstractRepository


class TasksService:
    def __init__(self, tasks_repository: AbstractRepository):
        self.tasks_repository = tasks_repository()

    async def create_task(self, task: TaskSchemaAdd) -> int:
        task_dict = task.model_dump()
        task_id = await self.tasks_repository.add_one(task_dict)

        if not task_id:
            raise HTTPException(status_code=500, detail="Failed to create task")

        return JSONResponse(
            status_code=201,
            content={"message": "Task created successfully", "id": str(task_id)},
        )

    async def get_tasks(self, status):
        filters = {}

        if status:
            filters["status"] = status

        tasks = await self.tasks_repository.get_all(**filters)
        if not tasks:
            raise HTTPException(status_code=404, detail="No tasks found")
        return tasks

    async def update_task(self, task_id: int, task: TaskSchemaUpdate):
        task_data = task.model_dump()

        updated_task = await self.tasks_repository.update(task_id, **task_data)
        if not updated_task:
            raise HTTPException(
                status_code=404, detail=f"Task with id {task_id} not found"
            )
        return updated_task

    async def delete_task(self, task_id: int):
        deleted_task_id = await self.tasks_repository.delete(task_id)
        if not deleted_task_id:
            raise HTTPException(
                status_code=404, detail=f"Task with id {task_id} not found"
            )
        return {"message": f"Task({deleted_task_id}) deleted successfully"}
