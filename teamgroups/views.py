import json

from django.views.generic import (
    ListView, CreateView, UpdateView, DetailView, DeleteView, RedirectView)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.views.generic import FormView
from django.core.urlresolvers import reverse
from django.contrib import messages

from guardian.mixins import LoginRequiredMixin, PermissionRequiredMixin

from allauth.account.adapter import get_adapter

from .models import TeamGroup, TeamGroupMembership, TeamGroupInvitation
from .forms import (
    TeamGroupCreateForm, TeamGroupUpdateForm, TeamGroupInvitationSendForm)

User = get_user_model()


class TeamGroupCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = TeamGroup
    form_class = TeamGroupCreateForm
    success_message = '%(name)s created successfully'

    def form_valid(self, form):
        teamgroup = form.save(commit=False)
        teamgroup.save()

        TeamGroupMembership.objects.create(
            teamgroup=teamgroup, member=self.request.user,
            role=TeamGroupMembership.ROLE_OWNER)

        return super(TeamGroupCreateView, self).form_valid(form)


class TeamGroupUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TeamGroup
    form_class = TeamGroupUpdateForm
    success_message = '%(name)s updated successfully'
    permission_required = 'teamgroups.change_teamgroup'
    raise_exception = True


class TeamGroupListView(LoginRequiredMixin, ListView):
    model = TeamGroup
    context_object_name = 'teamgroups'
    template_name = 'teamgroups/teamgroup_list.html'

    def get_queryset(self):
        return [t.teamgroup for t in self.request.user.teamgroupmembership_set.filter(
            active=True)]


class TeamGroupDetailView(PermissionRequiredMixin, DetailView):
    model = TeamGroup
    context_object_name = 'teamgroup'
    permission_required = 'teamgroups.view_teamgroup'
    raise_exception = True


class TeamGroupDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TeamGroup
    success_url = reverse_lazy('list_teamgroups')
    success_message = '%(name)s has been deleted'
    permission_required = 'teamgroups.delete_teamgroup'
    raise_exception = True


class TeamGroupLeaveView(PermissionRequiredMixin, SuccessMessageMixin, RedirectView):
    model = TeamGroup
    url = reverse_lazy('list_teamgroups')
    permanent = False
    success_message = 'You have been removed from %(name)s'
    permission_required = 'teamgroups.leave_teamgroup'
    raise_exception = True

    def get(self, request, *args, **kwargs):
        membership = TeamGroupMembership.objects.get(
            teamgroup=self.get_object(), member=self.request.user)
        membership.active = False
        membership.save()

        return super(TeamGroupLeaveView, self).get(self, *args, **kwargs)

    def get_object(self):
        return TeamGroup.objects.get(slug=self.kwargs['slug'])


class TeamGroupInvitationSendView(PermissionRequiredMixin, SuccessMessageMixin, FormView):
    model = TeamGroupInvitation
    form_class = TeamGroupInvitationSendForm
    template_name = 'teamgroups/teamgroupinvitation_form.html'
    success_message = 'Invitation sent to %(email)s'
    permission_required = 'teamgroups.view_teamgroup'
    raise_exception = True

    def get_object(self):
        self.teamgroup = TeamGroup.objects.get(slug=self.kwargs['slug'])
        return self.teamgroup

    def get_form_kwargs(self):
        kwargs = super(TeamGroupInvitationSendView, self).get_form_kwargs()
        kwargs['teamgroup'] = self.teamgroup
        return kwargs

    def form_valid(self, form):
        form.save(self.request.user)
        return super(TeamGroupInvitationSendView, self).form_valid(form)

    def get_success_url(self):
        return reverse('view_teamgroup', kwargs=self.kwargs)


class TeamGroupInvitationAcceptView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        try:
            invitation = TeamGroupInvitation.objects.get(
                accepted=False,
                key=self.kwargs['key'].lower())

            user = User.objects.get(email=invitation.email)
            invitation.accepted = True
            invitation.save()

            if invitation.teamgroup.is_member(user):
                messages.error(
                    self.request, 'You are already a member of this teamgroup')
            else:
                TeamGroupMembership.objects.create(
                    teamgroup=invitation.teamgroup, member=user,
                    role=TeamGroupMembership.ROLE_MEMBER)

                messages.success(
                    self.request,
                    'You are now a member of %s' % invitation.teamgroup)

            return reverse(
                'view_teamgroup', kwargs={'slug': invitation.teamgroup.slug})
        except User.DoesNotExist:
            get_adapter().stash_verified_email(self.request, invitation.email)
            return '%s?next=%s' % (
                reverse('account_signup'), self.request.get_full_path())
        except TeamGroupInvitation.DoesNotExist:
            messages.error(
                self.request, 'Invalid invitation key')

            return reverse('index')


class TeamGroupInvitationListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return TeamGroupInvitation.objects.filter(
            accepted=False, email=self.request.user.email)


class TeamGroupInvitationDeleteView(LoginRequiredMixin, DeleteView):
    model = TeamGroupInvitation

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse(json.dumps(TeamGroupInvitation.objects.filter(
            accepted=False, email=self.request.user.email).count()))
