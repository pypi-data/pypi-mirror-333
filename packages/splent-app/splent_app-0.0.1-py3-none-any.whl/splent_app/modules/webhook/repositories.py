from splent_app.modules.webhook.models import Webhook
from splent_framework.core.repositories.BaseRepository import BaseRepository


class WebhookRepository(BaseRepository):
    def __init__(self):
        super().__init__(Webhook)
