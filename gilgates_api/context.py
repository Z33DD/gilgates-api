from contextvars import ContextVar
from pydantic import BaseModel
from gilgates_api.dao.user import UserDAO


class ContextDAO(BaseModel):
    user: UserDAO = UserDAO()


context: ContextVar[ContextDAO] = ContextVar("dao", default=ContextDAO())
