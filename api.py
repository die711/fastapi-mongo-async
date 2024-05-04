from fastapi import FastAPI, Depends
from typing import Annotated

from routes.task import tasks_routes
from auth.auth import get_current_user
from routes.auth import auth_routes

app = FastAPI()
app.include_router(tasks_routes)
app.include_router(auth_routes)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str, ):
    return {"message": f"Hello {name}"}


@app.get("/hello/user/{name}")
async def say_hello(current_user: Annotated[dict, Depends(get_current_user)]):
    return {
        "message": f"Hello {current_user['username']}"
    }
