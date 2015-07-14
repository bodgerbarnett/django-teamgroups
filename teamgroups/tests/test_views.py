from django.test import TestCase

from teams.models import Team


class CreateTeamPageTest(TestCase):

    def test_create_team_page_renders_correct_template(self):
        response = self.client.get('/teams/create/')
        self.assertTemplateUsed(response, 'teams/create.html')

    def test_team_display_page_renders_correct_template(self):
        team = Team.objects.create()
        response = self.client.get('/teams/%d/' % team.id)
        self.assertTemplateUsed(response, 'teams/detail.html')
