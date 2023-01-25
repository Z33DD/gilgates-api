from datetime import datetime
from typing import Optional

import sqlalchemy as sql
from sqlalchemy.sql import func
from pydantic import EmailStr

from gilgates_api.database import metadata
from gilgates_api.model import Model
from gilgates_api.model.role import Role
# from gilgates_api.model.address import Address


user_table = sql.Table(
    "User",
    metadata,
    sql.Column("uid", sql.String(60), primary_key=True),
    sql.Column("created_at", sql.DateTime, nullable=False, server_default=func.now()),
    sql.Column("updated_at", sql.DateTime, onupdate=func.now()),
    sql.Column("last_login", sql.DateTime),
    sql.Column("ative", sql.Boolean, default=True),
    sql.Column("password", sql.String),
    sql.Column("role", sql.Enum(Role), default=Role.AGENTE, nullable=False),
    sql.Column("name", sql.String(120), nullable=True),
    sql.Column("cpf", sql.String(11), unique=True, nullable=True),
    sql.Column("email", sql.String(255), unique=True, nullable=False),
)

class User(Model):
    # Atributos funcionais
    last_login: Optional[datetime] = None
    ative: Optional[bool] = True
    password: Optional[str] = None
    role: Role = Role.AGENTE
    # Atributos naturais
    name: str
    cpf: Optional[str] = None
    email: EmailStr
    # address: Optional[Address]
