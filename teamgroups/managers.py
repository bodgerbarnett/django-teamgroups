from django.db import models
from django.utils.crypto import get_random_string


class TeamGroupInvitationManager(models.Manager):
    def create_invitation(self, teamgroup, inviter, email):
        key = get_random_string(64).lower()
        return self.create(
            teamgroup=teamgroup, inviter=inviter, email=email, key=key)
