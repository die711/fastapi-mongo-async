from typing import List
from bson import ObjectId

from schemes.task import Task, UpdateTask
from database.database import collection


async def get_all_tasks() -> List[Task]:
    tasks = []
    cursor = collection.find({})

    async for document in cursor:
        task = __collection_to_schema(document)
        tasks.append(task)

    return tasks


async def get_one_task_id(id: str) -> Task:
    task = await __get_task_by_id(id)
    if task is None:
        raise Exception('Task not found')

    return __collection_to_schema(task)


async def create_task(task: UpdateTask) -> Task:
    task_db = await __get_task_by_title(task.title)
    if task_db is not None:
        raise Exception('Task duplicated')

    new_task = await collection.insert_one(task.dict())
    print(f'new task: {new_task}')
    created_task = await __get_task_by_id(new_task.inserted_id)
    print(created_task)

    return __collection_to_schema(created_task)


async def update_task(id: str, data: UpdateTask) -> Task:
    task_db = __get_task_by_id(id)
    if task_db is None:
        raise Exception('Task not found')

    task_db = await __get_task_by_title(data.title)
    if task_db is not None:
        raise Exception('Task duplicated')

    # task = {k: v for k, v in data.dict().items() if v is not None}
    await collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    task_db = await __get_task_by_id(id)

    return task_db


async def delete_task(id: str) -> bool:
    task_db = __get_task_by_id(id)
    if task_db is None:
        raise Exception('Task not found')

    await collection.delete_one({"_id": ObjectId(id)})

    return True


def __collection_to_schema(task):
    return Task(
        id=str(task['_id']),
        title=task['title'],
        description=task['description'],
        completed=task['completed'],
    )


async def __get_task_by_id(id: str):
    return await collection.find_one({"_id": ObjectId(id)})


async def __get_task_by_title(title: str):
    return await collection.find_one({"title": title})