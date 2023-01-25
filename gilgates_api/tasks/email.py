from gilgates_api.worker import celery_factory


@celery_factory.task
def send_email(email: str):
    pass
