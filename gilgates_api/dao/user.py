from typing import List
from gilgates_api.dao import BaseDAO
from gilgates_api.model.user import user_table, User


class UserDAO(BaseDAO[User]):
    def __init__(self) -> None:
        super().__init__(user_table, User)

    async def get_by_email(self, email: str) -> User | None:
        users: List[User] | None = await self.query(self.table.c.email == email)
        if not users:
            return None
        return users[0]
