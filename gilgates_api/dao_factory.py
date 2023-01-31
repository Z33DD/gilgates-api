from typing import Optional
from pydantic import BaseModel
from sqlmodel import Session

from gilgates_api.dao.user import UserDAO


class Dao(BaseModel):
    user: UserDAO

    class Config:
        arbitrary_types_allowed = True


def dao_factory(session: Session) -> Dao:
    user_dao = UserDAO(session)
    dao = Dao(user=user_dao)
    return dao
