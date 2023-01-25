from celery import Celery
from gilgates_api.config import CELERY_CONFIG


def celery_factory() -> Celery:
    celery = Celery(__name__)
    celery.autodiscover_tasks(force=True)
    celery.conf.update(CELERY_CONFIG)

    return celery


celery = celery_factory()
