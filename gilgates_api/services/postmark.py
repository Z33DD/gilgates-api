from postmarker.core import PostmarkClient
from gilgates_api.config import POSTMARK_API_TOKEN

# [Python Postmaker Docs](https://postmarker.readthedocs.io/en/stable)
postmark = PostmarkClient(server_token=POSTMARK_API_TOKEN)
