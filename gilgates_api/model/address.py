from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class Address(BaseModel):
    uid: UUID
    created_at: datetime
    lat: float
    lng: float
