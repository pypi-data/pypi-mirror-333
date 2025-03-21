from splent_app.modules.profile.models import UserProfile
from splent_framework.core.repositories.BaseRepository import BaseRepository


class UserProfileRepository(BaseRepository):
    def __init__(self):
        super().__init__(UserProfile)
