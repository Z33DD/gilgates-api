from uuid import UUID, uuid4
from datetime import date, datetime
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
    city: str
    state: State
    postal_code: str
    street: str
    house_number: Optional[str]
    extra_info: Optional[str]
    lat: Optional[float]
    lng: Optional[float]


class LegalEntity(Model, table=True):
    name: str
    cnpj: str = Field(unique=True)
    owner: UUID = Field(foreign_key="user.uid")
    address_uid: Optional[UUID] = Field(foreign_key="address.uid", default=None)
    # Relationships
    address: Address = Relationship()
    employees: List["Employee"] = Relationship(back_populates="legal_entity")


class Customer(Model, table=True):
    name: str
    phone: List[str]
    email: Optional[EmailStr]
    employee_id: UUID = Field(foreign_key="user.uid", default=None)
    address_uid: Optional[UUID] = Field(foreign_key="address.uid", default=None)
    employee: "User" = Relationship(back_populates="customers")
    address: Address = Relationship()

    @validator("phone")
    def phone_validator(cls, numbers: List[str]):
        for number in numbers:
            phone = phonenumbers.parse(number, "BR")
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
    # Relationships
    customers: List[Customer] = Relationship(back_populates="employee")
    address: Address = Relationship()


class Employee(Model, table=True):
    ativo: bool = True
    nome: str
    cpf: str
    rg: str
    orgao_expedidor: str
    chavej: str
    email: EmailStr
    empresa: str
    data_nasc: str
    tam_camisa: str
    data_inicio: date
    legal_entity_id: Optional[UUID] = Field(foreign_key="legal_entity.uid", default=None)
    legal_entity: LegalEntity = Relationship(back_populates="employees")
    address_uid: Optional[UUID] = Field(foreign_key="address.uid", default=None)
    address: Address = Relationship()
