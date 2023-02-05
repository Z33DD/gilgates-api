from gilgates_api import worker as celery
from gilgates_api.dao_factory import dao_factory
from gilgates_api.settings import get_settings
from gilgates_api.logger import logger as logger

config = get_settings()

__version__ = "2.0.0"
