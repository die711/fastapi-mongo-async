from fastapi import APIRouter, HTTPException

from database.database import (
    get_all_tasks,
    get_one_task,
    get_one_task_id,
    create_task,
    update_task,
    delete_task
)
from schemes.task import Task, UpdateTask

tasks_routes = APIRouter(prefix='/api/tasks', tags=['tasks'])


@tasks_routes.get('/')
async def get_tasks():
    response = await get_all_tasks()
    return response


@tasks_routes.get('/{id}', response_model=Task)
async def get_task(id: str):
    response = await get_one_task_id(id)
    if response:
        return response
    raise HTTPException(404, f"There is no task with the id {id}")


@tasks_routes.post('/', response_model=Task)
async def save_task(task: Task):
    task_found = await get_one_task(task.title)
    if task_found:
        raise HTTPException(409, "Task already exists")
    #
    response = await create_task(task.dict())
    if response:
        return response

    raise HTTPException(400, "Something went wrong")


@tasks_routes.put('/', response_model=Task)
async def put_task(id: str, data: UpdateTask):
    response = await update_task(id, data)
    if response:
        return response
    raise HTTPException(404, f"There is no task with the id {id}")


@tasks_routes.delete('/{id}')
async def remove_task(id: str):
    response = await delete_task(id)
    if response:
        return "Successfully deleted task"
    raise HTTPException(404, f"There is no task with the id {id}")
