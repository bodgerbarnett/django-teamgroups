from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.text import slugify

from guardian.shortcuts import assign_perm


class TeamGroup(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='TeamGroupMembership')

    class Meta:
        permissions = (
            ('view_TeamGroup', 'Can view TeamGroup'),
            ('leave_TeamGroup', 'Can leave TeamGroup'),
        )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('view_TeamGroup', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        super(TeamGroup, self).save(*args, **kwargs)

    def is_member(self, user):
        return user in self.members.all()

    @property
    def active_members(self):
        return self.members.filter(TeamGroupmembership__active=True)


class TeamGroupMembership(models.Model):

    ROLE_MEMBER = 'member'
    ROLE_MANAGER = 'manager'
    ROLE_OWNER = 'owner'

    ROLE_CHOICES = [
        (ROLE_MEMBER, 'member'),
        (ROLE_MANAGER, 'manager'),
        (ROLE_OWNER, 'owner')
    ]

    TeamGroup = models.ForeignKey(TeamGroup)
    member = models.ForeignKey(settings.AUTH_USER_MODEL)
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default=ROLE_MEMBER)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return 'TeamGroup: %s, Member: %s, Active: %s' % (self.TeamGroup, self.member, self.active)

    def save(self, *args, **kwargs):
        if not self.id:
            assign_perm('view_TeamGroup', self.member, self.TeamGroup)

            if self.role == self.ROLE_OWNER:
                assign_perm('change_TeamGroup', self.member, self.TeamGroup)
                assign_perm('delete_TeamGroup', self.member, self.TeamGroup)
            else:
                assign_perm('leave_TeamGroup', self.member, self.TeamGroup)

        super(TeamGroupMembership, self).save(*args, **kwargs)
