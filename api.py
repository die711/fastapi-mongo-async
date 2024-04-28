from fastapi import FastAPI

from routes.task import tasks_routes

app = FastAPI()
app.include_router(tasks_routes)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
