from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId as _ObjectId

from typing_extensions import Annotated

from pydantic import BaseModel, ValidationError, field_validator
from pydantic.functional_validators import AfterValidator


def check_object_id(value: str) -> str:
    if not _ObjectId.is_valid(value):
        raise ValueError('Invalid ObjectId')
    return value


ObjectId = Annotated[str, AfterValidator(check_object_id)]


class Task(BaseModel):
    id: str
    title: str = Field(min_length=5, max_length=20)
    description: str
    completed: bool = False

    class Config:
        pass


class UpdateTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

    class Config:
        pass
