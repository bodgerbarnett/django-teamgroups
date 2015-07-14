from django import forms
from django.contrib.auth import get_user_model

from .models import TeamGroup, TeamGroupInvitation

User = get_user_model()


class TeamGroupCreateForm(forms.ModelForm):
    class Meta:
        model = TeamGroup
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data['name']

        if TeamGroup.objects.filter(name=name).exists():
            raise forms.ValidationError(
                '%(name)s already exists',
                params={'name': name})

        return name


class TeamGroupUpdateForm(forms.ModelForm):
    class Meta:
        model = TeamGroup
        fields = ['name']


class TeamGroupInvitationSendForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        self.teamgroup = kwargs.pop('teamgroup')
        super(TeamGroupInvitationSendForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']

        if TeamGroupInvitation.objects.filter(accepted=False, email__iexact=email):
            raise forms.ValidationError(
                '%(user)s has already been invited to %(teamgroup)s',
                params={'user': email, 'teamgroup': self.teamgroup})

        if TeamGroup.objects.filter(members__email=email, id=self.teamgroup.id).exists():
            raise forms.ValidationError(
                '%(user)s is already a member of this teamgroup',
                params={'user': email})

        return email

    def save(self, inviter):
        invitation = TeamGroupInvitation.objects.create_invitation(
            teamgroup=self.teamgroup, inviter=inviter, email=self.cleaned_data['email'])
        invitation.send()
        return invitation
