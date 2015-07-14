
from django.views.generic import (
    ListView, CreateView, UpdateView, DetailView, DeleteView, RedirectView)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy

from guardian.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import TeamGroup, TeamGroupMembership
from .forms import TeamGroupCreateForm, TeamGroupUpdateForm

User = get_user_model()


class TeamGroupCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = TeamGroup
    form_class = TeamGroupCreateForm
    success_message = '%(name)s created successfully'

    def form_valid(self, form):
        TeamGroup = form.save(commit=False)
        TeamGroup.save()

        TeamGroupMembership.objects.create(
            TeamGroup=TeamGroup, member=self.request.user,
            role=TeamGroupMembership.ROLE_OWNER)

        return super(TeamGroupCreateView, self).form_valid(form)


class TeamGroupUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TeamGroup
    form_class = TeamGroupUpdateForm
    success_message = '%(name)s updated successfully'
    permission_required = 'TeamGroups.change_TeamGroup'
    raise_exception = True


class TeamGroupListView(LoginRequiredMixin, ListView):
    model = TeamGroup
    context_object_name = 'TeamGroups'
    template_name = 'TeamGroups/TeamGroup_list.html'

    def get_queryset(self):
        return [t.TeamGroup for t in self.request.user.TeamGroupmembership_set.filter(
            active=True)]


class TeamGroupDetailView(PermissionRequiredMixin, DetailView):
    model = TeamGroup
    context_object_name = 'TeamGroup'
    permission_required = 'TeamGroups.view_TeamGroup'
    raise_exception = True


class TeamGroupDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TeamGroup
    success_url = reverse_lazy('list_TeamGroups')
    success_message = '%(name)s has been deleted'
    permission_required = 'TeamGroups.delete_TeamGroup'
    raise_exception = True


class TeamGroupLeaveView(PermissionRequiredMixin, SuccessMessageMixin, RedirectView):
    model = TeamGroup
    url = reverse_lazy('list_TeamGroups')
    permanent = False
    success_message = 'You have been removed from %(name)s'
    permission_required = 'TeamGroups.leave_TeamGroup'
    raise_exception = True

    def get(self, request, *args, **kwargs):
        membership = TeamGroupMembership.objects.get(
            TeamGroup=self.get_object(), member=self.request.user)
        membership.active = False
        membership.save()

        return super(TeamGroupLeaveView, self).get(self, *args, **kwargs)

    def get_object(self):
        return TeamGroup.objects.get(slug=self.kwargs['slug'])
