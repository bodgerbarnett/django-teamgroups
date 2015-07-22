from django import template

from .models import TeamGroupMembership

register = template.Library()


@register.simple_tag
def user_role(user, teamgroup):
    return TeamGroupMembership.objects.get(teamgroup=teamgroup, member=user).role
