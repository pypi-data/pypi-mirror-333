from pydantic import BaseModel


class Unknown(BaseModel):
    cause: str
