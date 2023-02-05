from sqlmodel import create_engine
from gilgates_api.settings import config


def engine_factory():
    engine = create_engine(
        config.database_url,
        echo=config.debug,
        connect_args=config.connect_args,
    )

    return engine


engine = engine_factory()
