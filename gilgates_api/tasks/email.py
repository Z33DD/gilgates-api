from gilgates_api.worker import app
from gilgates_api.services.postmark import postmark


@app.task
def send_email(
    email: str,
):
    email = postmark.emails.Email(
        From="pedro@z33dd.com",
        To=email,
        Subject="Postmark test",
        HtmlBody="<html><body><strong>Hello</strong> dear Postmark user.</body></html>",
    )
