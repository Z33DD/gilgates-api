from typing import Optional
from celery import Celery
from gilgates_api.settings import get_settings
from gilgates_api.settings import Settings


def celery_factory(config: Optional[Settings] = None) -> Celery:
    if not config:
        config = get_settings()
    celery = Celery(
        "gilgates_api",
        include=["gilgates_api.tasks"],
        broker=config.celery_broker_url,
        backend=config.celery_result_backend,
    )
    celery.autodiscover_tasks(force=True)

    return celery


app = celery_factory()

if __name__ == "__main__":
    app.start()
