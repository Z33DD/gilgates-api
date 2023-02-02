from enum import Enum, auto
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import EmailStr


class Model(SQLModel):
    uid: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Creation date of this record"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Last update date of this record"
    )


class Role(str, Enum):
    ADMIN = auto()
    SUPERVISOR = auto()
    AGENTE = auto()
    ANON = auto()


class User(Model, table=True):
    # Functional attributes
    last_login: Optional[datetime] = None
    ative: Optional[bool] = True
    password: Optional[str] = None
    role: Role = Role.AGENTE
    # Natural attributes
    name: str
    cpf: Optional[str] = None
    email: EmailStr
