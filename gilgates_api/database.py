from sqlmodel import create_engine, SQLModel
from gilgates_api import config

engine = create_engine(config.DATABASE_URL, echo=config.DEBUG)


def create_tables() -> None:
    SQLModel.metadata.create_all(engine)
