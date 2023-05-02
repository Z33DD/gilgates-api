from datetime import date
from fastapi import Depends, APIRouter, Query
from sqlmodel import Session
from pydantic import BaseModel, EmailStr
from gilgates_api.deps import current_user, get_session
from gilgates_api.model import User, Customer, Employee
from gilgates_api import dao_factory

router = APIRouter()


class EmployeeIn(BaseModel):
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


@router.get("/", response_model=list[Employee])
async def read_employees(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    dao = dao_factory(session)
    employees = await dao.employee.get_all(limit, offset)
    return employees


@router.post("/", response_model=Customer)
async def create_employee(
    data: EmployeeIn,
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    dao = dao_factory(session)

    employee = Employee(
        ativo=data.ativo,
        nome=data.nome,
        cpf=data.cpf,
        rg=data.rg,
        orgao_expedidor=data.orgao_expedidor,
        chavej=data.chavej,
        email=data.email,
        empresa=data.empresa,
        data_nasc=data.data_nasc,
        tam_camisa=data.tam_camisa,
        data_inicio=data.data_inicio,
    )

    await dao.employee.create(employee)
    dao.commit()

    return employee


@router.put("/", response_model=Customer)
async def update_employee(
    data: EmployeeIn,
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    dao = dao_factory(session)

    employee = Employee(
        ativo=data.ativo,
        nome=data.nome,
        cpf=data.cpf,
        rg=data.rg,
        orgao_expedidor=data.orgao_expedidor,
        chavej=data.chavej,
        email=data.email,
        empresa=data.empresa,
        data_nasc=data.data_nasc,
        tam_camisa=data.tam_camisa,
        data_inicio=data.data_inicio,
    )

    await dao.employee.update(employee)
    dao.commit()

    return employee
