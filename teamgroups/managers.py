from django.db import models
from django.utils.crypto import get_random_string


class TeamGroupMembershipManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class TeamGroupInvitationQuerySet(models.query.QuerySet):
    def pending(self):
        return self.filter(accepted=False)


class TeamGroupInvitationManager(models.Manager):
    use_for_related_fields = True

    def create_invitation(self, teamgroup, inviter, email):
        key = get_random_string(64).lower()

        return self.create(
            teamgroup=teamgroup, inviter=inviter, email=email, key=key)

    def get_queryset(self):
        return TeamGroupInvitationQuerySet(self.model, using=self._db)

    def pending(self):
        return self.get_queryset().pending()
