from typing import Optional
from pydantic import BaseModel, Field


class Task(BaseModel):
    id: str
    title: str
    description: str
    completed: bool = False


class UpdateTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
