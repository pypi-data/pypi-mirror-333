from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class Base(BaseModel, Generic[T]):
    success: bool
    data: T
    message: str
