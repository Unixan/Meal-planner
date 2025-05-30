from pydantic import BaseModel
from uuid import UUID

class TestEntryCreate(BaseModel):
    id: UUID
    name: str
    note: str | None = None

class TestEntryOut(BaseModel):
    id: UUID
    name: str
    note: str | None = None

    class Config:
        orm_mode = True