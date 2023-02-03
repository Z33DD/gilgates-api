from uuid import UUID, uuid4
from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr, validator
import phonenumbers
from gilgates_api.enums import Role, State


class Model(SQLModel):
    uid: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Creation date of this record"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Last update date of this record"
    )


class Address(Model, table=True):
    lat: float
    lng: float
    city: str
    state: State


class Company(Model, table=True):
    name: str
    cnpj: str = Field(unique=True)
    address_uid: Optional[UUID] = Field(foreign_key="address.uid", default=None)
    # Relationships
    address: Address = Relationship()
    employees: List["User"] = Relationship(back_populates="company")


class Customer(Model, table=True):
    name: str
    phone: str
    employee_id: UUID = Field(foreign_key="user.uid", default=None)
    address_uid: Optional[UUID] = Field(foreign_key="address.uid", default=None)
    employee: "User" = Relationship(back_populates="customers")
    address: Address = Relationship()

    @validator("phone")
    def phone_validator(cls, numbers):
        phone = phonenumbers.parse(numbers, "BR")
        assert phonenumbers.is_valid_number(phone)
        return numbers


class User(Model, table=True):
    # Functional attributes
    last_login: Optional[datetime] = None
    ative: Optional[bool] = True
    password: Optional[str] = None
    role: Role = Role.EMPLOYEE
    # Natural attributes
    name: str
    cpf: Optional[str] = None
    email: EmailStr
    # Foreign keys
    address_uid: Optional[UUID] = Field(foreign_key="address.uid", default=None)
    company_id: Optional[UUID] = Field(foreign_key="company.uid", default=None)
    # Relationships
    customers: List[Customer] = Relationship(back_populates="employee")
    address: Address = Relationship()
    company: Company = Relationship(back_populates="employees")
