from django.conf.urls import patterns, url

from .views import (
    TeamGroupListView, TeamGroupCreateView, TeamGroupUpdateView,
    TeamGroupDeleteView, TeamGroupDetailView, TeamGroupLeaveView,
    TeamGroupInvitationSendView, TeamGroupInvitationAcceptView,
    TeamGroupInvitationListView, TeamGroupInvitationDeleteView,
    TeamGroupInvitationResendView, TeamGroupMembershipUpdateView)


urlpatterns = patterns(
    'teamgroups.views',

    url(
        r'^list/$',
        TeamGroupListView.as_view(),
        name='list_teamgroups'),

    url(
        r'^create/$',
        TeamGroupCreateView.as_view(),
        name='create_teamgroup'),

    url(
        r'^view/(?P<slug>[\w\-]+)/$',
        TeamGroupDetailView.as_view(),
        name='view_teamgroup'),

    url(
        r'^edit/(?P<slug>[\w\-]+)/$',
        TeamGroupUpdateView.as_view(),
        name='edit_teamgroup'),

    url(
        r'^leave/(?P<slug>[\w\-]+)/$',
        TeamGroupLeaveView.as_view(),
        name='leave_teamgroup'),

    url(
        r'^delete/(?P<slug>[\w\-]+)$',
        TeamGroupDeleteView.as_view(),
        name='delete_teamgroup'),

    url(
        r'^member/edit/(?P<pk>\w+)$',
        TeamGroupMembershipUpdateView.as_view(),
        name='edit_member'),

    url(r'^invites/send/(?P<slug>[\w\-]+)/$',
        TeamGroupInvitationSendView.as_view(),
        name='send_invitation'),

    url(r'^invites/resend/(?P<pk>\w+)/$',
        TeamGroupInvitationResendView.as_view(),
        name='resend_invitation'),

    url(r'^invites/accept/(?P<key>\w+)/$',
        TeamGroupInvitationAcceptView.as_view(),
        name='accept_invitation'),

    url(
        r'^invites/list/$',
        TeamGroupInvitationListView.as_view(),
        name='list_invitations'),

    url(
        r'^invites/delete/(?P<pk>\w+)/$',
        TeamGroupInvitationDeleteView.as_view(),
        name='delete_invitation'),
)
