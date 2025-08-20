from src.repositories.tasks import TasksRepository
from src.services.tasks import TasksService


def get_tasks_service():
    return TasksService(TasksRepository)
