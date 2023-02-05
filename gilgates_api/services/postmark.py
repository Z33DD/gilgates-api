from postmarker.core import PostmarkClient
from fastapi import Depends
from gilgates_api.settings import get_settings
from gilgates_api.settings import Settings


def postmark_factory(config: Settings = Depends(get_settings)) -> PostmarkClient:
    try:
        token = config.postmark_api_token
    except AttributeError:
        config = get_settings()
        token = config.postmark_api_token

    return PostmarkClient(server_token=token)


# [Python Postmaker Docs](https://postmarker.readthedocs.io/en/stable)
postmark = postmark_factory()
