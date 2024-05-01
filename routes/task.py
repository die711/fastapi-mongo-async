from typing import List

from fastapi import APIRouter, HTTPException

from database.task import crud
from schemes.task import Task, UpdateTask

tasks_routes = APIRouter(prefix='/api/tasks', tags=['tasks'])


@tasks_routes.get('/', response_model=List[Task])
async def get_tasks():
    response = await crud.get_all_tasks()
    return response


@tasks_routes.get('/{id}', response_model=Task)
async def get_task(id: str):
    try:
        response = await crud.get_one_task_id(id)
        return response

    except Exception as e:
        raise HTTPException(404, str(e))


@tasks_routes.post('/', response_model=Task)
async def save_task(task: UpdateTask):
    try:
        response = await crud.create_task(task)
        return response

    except Exception as e:
        raise HTTPException(400, str(e))


@tasks_routes.put('/{id}', response_model=Task)
async def put_task(id: str, data: UpdateTask):
    try:
        response = await crud.update_task(id, data)
        return response
    except Exception as e:
        raise HTTPException(400, str(e))

#
#
# @tasks_routes.delete('/{id}')
# async def remove_task(id: str):
#     response = await delete_task(id)
#     if response:
#         return "Successfully deleted task"
#     raise HTTPException(404, f"There is no task with the id {id}")
