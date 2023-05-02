from pydantic import BaseModel
from sqlmodel import Session

from gilgates_api.dao import BaseDAO
from gilgates_api.dao.user import UserDAO
from gilgates_api.model import LegalEntity, Customer, Employee


class MasterDAO(BaseModel):
    user: UserDAO
    company: BaseDAO[LegalEntity]
    customer: BaseDAO[Customer]
    employee: BaseDAO[Employee]

    class Config:
        arbitrary_types_allowed = True

    def commit(self) -> None:
        self.user.commit()
        self.company.commit()
        self.customer.commit()


def dao_factory(session: Session) -> MasterDAO:
    user_dao = UserDAO(session)
    company_dao = BaseDAO(session, LegalEntity)
    customer_dao = BaseDAO(session, Customer)
    employee_dao = BaseDAO(session, Employee)

    dao = MasterDAO(
        user=user_dao,
        company=company_dao,
        customer=customer_dao,
        employee=employee_dao,
    )
    return dao
