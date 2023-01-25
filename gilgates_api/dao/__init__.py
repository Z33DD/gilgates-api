from typing import Any, Dict, Generic, List, TypeVar
import uuid
from sqlalchemy import Table
from gilgates_api.database import db
from gilgates_api.model import Model

T = TypeVar("T")


class BaseDAO(Generic[T]):
    cache: Dict[uuid.UUID, T]
    table: Table
    schema: Model

    def __init__(self, table: Table, schema: Model) -> None:
        """
        The __init__ function is called automatically when a new instance of the class is created.
        It sets up the object with all of the attributes that were defined in its signature.


        :param self: Refer to the instance of the class
        :param table: Table: Specify the table that is being mapped
        :param schema: Model: Define the model that this table is associated with
        :return: Nothing
        :doc-author: Trelent
        """
        self.table = table
        self.schema = schema
        self.cache = {}

    async def read(self, ids: List[uuid.UUID]) -> None:
        ids = [str(a) for a in ids]
        query = self.table.select().where(self.table.c.uid.in_(ids))
        items = await db.fetch_all(query)
        for item in items:
            item = dict(item)
            obj = self.__make_object(item)
            self.cache.update({uuid.UUID(item["uid"]): obj})

    async def get(self, item_id: uuid.UUID) -> T | None:
        if item_id not in self.cache.keys():
            await self.read([item_id])
        return self.cache.get(item_id)

    async def delete(self, item_id: uuid.UUID) -> None:
        query = self.table.delete().where(self.table.c.uid == str(item_id))
        self.cache.pop(item_id, None)
        await db.execute(query)

    async def create(self, item: Model) -> uuid.UUID:
        values = item.dict()
        values["uid"] = str(item.uid)
        query = self.table.insert(values)
        self.cache.update({item.uid: item})

        await db.execute(query)
        return item.uid

    async def update(self, item: Model) -> None:
        values = item.dict()
        item_id = str(item.uid)
        values["uid"] = item_id
        query = self.table.update(self.table.c.uid == item_id, values)
        await db.execute(query)

    async def get_all(self) -> List[T]:
        query = self.table.select()
        result = await db.execute(query)
        return self.__make_objects(result)
    
    def clear(self) -> None:
        self.cache = {}

    def __make_object(self, data: Dict[str, Any]) -> T:
        return self.schema.parse_obj(data)

    def __make_objects(self, data: List[Dict[str, Any]]) -> List[T]:
        items = []
        for raw in data:
            items.append(self.__make_object(raw))
        return items
