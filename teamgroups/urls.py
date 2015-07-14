from django.conf.urls import patterns, url

from .views import (
    TeamGroupListView, TeamGroupCreateView, TeamGroupUpdateView, TeamGroupDeleteView,
    TeamGroupDetailView, TeamGroupLeaveView)


urlpatterns = patterns(
    'TeamGroup.views',

    url(
        r'^list/$',
        TeamGroupListView.as_view(),
        name='list_TeamGroups'),

    url(
        r'^create/$',
        TeamGroupCreateView.as_view(),
        name='create_TeamGroup'),

    url(
        r'^(?P<slug>[\w\-]+)/$',
        TeamGroupDetailView.as_view(),
        name='view_TeamGroup'),

    url(
        r'^edit/(?P<slug>[\w\-]+)/$',
        TeamGroupUpdateView.as_view(),
        name='edit_TeamGroup'),

    url(
        r'^leave/(?P<slug>[\w\-]+)/$',
        TeamGroupLeaveView.as_view(),
        name='leave_TeamGroup'),

    url(
        r'^delete/(?P<slug>[\w\-]+)$',
        TeamGroupDeleteView.as_view(),
        name='delete_TeamGroup')
)
