from typing import List
from pydantic import BaseModel

from tpauth.response.base import Base


class Data(BaseModel):
    auth: bool
    id: int
    token: str
    name: str
    alias: str
    email: str
    phone: str
    roles: List[str]
    permissions: List[str]


class Success(Base[Data]):
    pass


class FromTokenUnauthoried(Base[Data]):
    pass
