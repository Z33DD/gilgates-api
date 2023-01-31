from celery import Celery
from gilgates_api.config import CELERY_CONFIG


def celery_factory() -> Celery:
    celery = Celery(
        "gilgates_api",
        include=['gilgates_api.tasks']
        )
    celery.autodiscover_tasks(force=True)
    celery.conf.update(CELERY_CONFIG)

    return celery


app = celery_factory()

if __name__ == '__main__':
    app.start()
