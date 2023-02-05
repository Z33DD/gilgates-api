from typing import Dict
from gilgates_api.worker import app
from gilgates_api.services.postmark import postmark
from gilgates_api import settings


TEMPLATES = {"welcome": 30630498}


@app.task()
def send_email(email: str, template: str, template_data: Dict[str, str]):
    template_id = TEMPLATES.get(template)

    if not template_id:
        raise RuntimeError(f"Template {template} doesn't exists")
    
    if settings.ENV != "production":
        return

    postmark.emails.send_with_template(
        TemplateId=template_id,
        TemplateModel=template_data,
        From="pedro@z33dd.com",
        To=email,
    )
