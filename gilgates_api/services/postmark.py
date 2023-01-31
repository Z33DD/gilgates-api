from postmarker.core import PostmarkClient
from gilgates_api.config import POSTMARK_API_TOKEN

postmark = PostmarkClient(server_token=POSTMARK_API_TOKEN)
