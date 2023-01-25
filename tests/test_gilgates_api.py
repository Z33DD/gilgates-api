from gilgates_api import __version__
from gilgates_api.database import create_tables
from gilgates_api.config import VERSION
import pytest


def test_version():
    assert __version__ == VERSION

@pytest.mark.skip(reason="No need to run this every time")
async def test_create_table():
    await create_tables()
