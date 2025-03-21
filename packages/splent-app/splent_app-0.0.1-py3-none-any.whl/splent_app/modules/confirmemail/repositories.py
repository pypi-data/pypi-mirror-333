from splent_app.modules.confirmemail.models import Confirmemail
from splent_framework.core.repositories.BaseRepository import BaseRepository


class ConfirmemailRepository(BaseRepository):
    def __init__(self):
        super().__init__(Confirmemail)
