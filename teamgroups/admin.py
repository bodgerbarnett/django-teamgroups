from django.contrib import admin

from .models import TeamGroup, TeamGroupMembership, TeamGroupInvitation


class TeamGroupMembershipInline(admin.TabularInline):
    model = TeamGroupMembership


class TeamGroupAdmin(admin.ModelAdmin):
    inlines = (TeamGroupMembershipInline,)


class TeamGroupInvitationAdmin(admin.ModelAdmin):
    pass

admin.site.register(TeamGroup, TeamGroupAdmin)
admin.site.register(TeamGroupInvitation, TeamGroupInvitationAdmin)
