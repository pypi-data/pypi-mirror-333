from splent_app.modules.reset.models import ResetToken
from splent_framework.core.repositories.BaseRepository import BaseRepository


class ResetRepository(BaseRepository):
    def __init__(self):
        super().__init__(ResetToken)
