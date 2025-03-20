from pydantic import BaseModel

from tpauth.response.base import Base


class Data(BaseModel):
    error: str


class Unauthorised(Base[Data]):
    pass
