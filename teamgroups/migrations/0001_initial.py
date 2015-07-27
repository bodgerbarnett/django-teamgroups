# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'permissions': (('view_teamgroup', 'Can view teamgroup'),),
            },
        ),
        migrations.CreateModel(
            name='TeamGroupInvitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('accepted', models.BooleanField(default=False)),
                ('key', models.CharField(unique=True, max_length=64)),
                ('date_invited', models.DateTimeField(default=django.utils.timezone.now)),
                ('inviter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('teamgroup', models.ForeignKey(related_name='invitations', to='teamgroups.TeamGroup')),
            ],
        ),
        migrations.CreateModel(
            name='TeamGroupMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(default=b'member', max_length=20, choices=[(b'owner', b'<strong>Owner</strong><br>The person who is            the primary contact for the team group. Owners can modify or            delete the team group.'), (b'manager', b'<strong>Manager</strong><br>Allowed to            modify the team group.'), (b'member', b'<strong>Member</strong><br>Can view the             team group but is not allowed to modify it.')])),
                ('active', models.BooleanField(default=True)),
                ('member', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('teamgroup', models.ForeignKey(related_name='memberships', to='teamgroups.TeamGroup')),
            ],
        ),
        migrations.AddField(
            model_name='teamgroup',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='teamgroups.TeamGroupMembership'),
        ),
    ]
