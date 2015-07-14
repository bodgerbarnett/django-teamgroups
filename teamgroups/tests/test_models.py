from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from teams.models import Team

User = get_user_model()


class TeamModelTest(TestCase):
    def test_team_has_owner(self):
        Team(owner=User.objects.create())

    def test_user_cannot_create_duplicate_teams(self):
        user = User.objects.create()
        Team.objects.create(name='Team One', owner=user)

        with self.assertRaises(ValidationError):
            Team.objects.create(name='Team One', owner=user)
