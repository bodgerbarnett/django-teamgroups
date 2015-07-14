from django import forms
from django.contrib.auth import get_user_model

from .models import TeamGroup

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
