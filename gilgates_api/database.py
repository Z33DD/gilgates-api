import databases
import sqlalchemy

from gilgates_api import config

db = databases.Database(config.DATABASE_URL)
metadata = sqlalchemy.MetaData()


async def create_tables() -> None:
    if config.ENV == "development":
        dialect = sqlalchemy.dialects.sqlite.dialect()
    else:
        dialect = sqlalchemy.dialects.postgresql.dialect()
    for table in metadata.tables.values():
        # Set `if_not_exists=False` if you want the query to throw an
        # exception when the table already exists
        schema = sqlalchemy.schema.CreateTable(table, if_not_exists=True)
        query = str(schema.compile(dialect=dialect))
        await db.execute(query=query)
