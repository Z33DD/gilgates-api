from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class Model(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
