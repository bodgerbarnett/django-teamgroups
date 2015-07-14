from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.template import TemplateDoesNotExist
from django.core.mail import EmailMultiAlternatives, EmailMessage

from guardian.shortcuts import assign_perm

from .managers import TeamGroupInvitationManager
from .signals import invitation_sent


class TeamGroup(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='TeamGroupMembership')

    class Meta:
        permissions = (
            ('view_teamgroup', 'Can view teamgroup'),
        )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('view_teamgroup', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        super(TeamGroup, self).save(*args, **kwargs)

    def is_member(self, user):
        return user in self.members.all()

    @property
    def active_members(self):
        return self.members.filter(teamgroupmembership__active=True)


class TeamGroupMembership(models.Model):

    ROLE_MEMBER = 'member'
    ROLE_MANAGER = 'manager'
    ROLE_OWNER = 'owner'

    ROLE_CHOICES = [
        (ROLE_MEMBER, 'member'),
        (ROLE_MANAGER, 'manager'),
        (ROLE_OWNER, 'owner')
    ]

    teamgroup = models.ForeignKey(TeamGroup)
    member = models.ForeignKey(settings.AUTH_USER_MODEL)
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default=ROLE_MEMBER)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return 'TeamGroup: %s, Member: %s, Active: %s' % (
            self.teamgroup, self.member, self.active)

    def save(self, *args, **kwargs):
        if not self.id:
            assign_perm('view_teamgroup', self.member, self.teamgroup)

            if self.role == self.ROLE_OWNER:
                assign_perm('change_teamgroup', self.member, self.teamgroup)
                assign_perm('delete_teamgroup', self.member, self.teamgroup)

        super(TeamGroupMembership, self).save(*args, **kwargs)


class TeamGroupInvitation(models.Model):
    teamgroup = models.ForeignKey(TeamGroup)
    email = models.EmailField()
    accepted = models.BooleanField(default=False)
    key = models.CharField(max_length=64, unique=True)
    date_invited = models.DateTimeField(default=timezone.now)
    inviter = models.ForeignKey(settings.AUTH_USER_MODEL)

    objects = TeamGroupInvitationManager()

    def __unicode__(self):
        return '%s has invited you to join %s' % (
            self.inviter.get_full_name(),
            self.teamgroup.name)

    def get_absolute_url(self):
        return reverse('view_teamgroup', args=[str(self.team.id)])

    def send(self):
        template_prefix = 'teamgroups/emails/invitation'
        context = {
            'inviter': self.inviter,
            'teamgroup': self.teamgroup,
            'invitation_url': reverse(
                'accept_invitation',
                kwargs=dict(key=self.key)),
            'site': Site.objects.get_current()}
        subject = render_to_string(
            '%s_subject.txt' % template_prefix, context)

        # remove superfluous line breaks
        subject = ' '.join(subject.splitlines()).strip()

        bodies = {}

        for ext in ['html', 'txt']:
            try:
                template_name = '%s_message.%s' % (template_prefix, ext)
                bodies[ext] = render_to_string(
                    template_name, context).strip()
            except TemplateDoesNotExist:
                if ext == 'txt' and not bodies:
                    # We need at least one body
                    raise

        if 'txt' in bodies:
            msg = EmailMultiAlternatives(
                subject, bodies['txt'],
                settings.DEFAULT_FROM_EMAIL, [self.email])

            if 'html' in bodies:
                msg.attach_alternative(bodies['html'], 'text/html')
        else:
            msg = EmailMessage(
                subject, bodies['html'],
                settings.DEFAULT_FROM_EMAIL, [self.email])
            msg.content_subtype = 'html'

        msg.send()

        invitation_sent.send(sender=self.__class__, instance=self)
