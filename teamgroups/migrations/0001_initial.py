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
                'permissions': (('view_teamgroup', 'Can view teamgroup'), ('leave_teamgroup', 'Can leave teamgroup')),
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
                ('teamgroup', models.ForeignKey(to='teamgroups.TeamGroup')),
            ],
        ),
        migrations.CreateModel(
            name='TeamGroupMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(default=b'member', max_length=20, choices=[(b'member', b'member'), (b'manager', b'manager'), (b'owner', b'owner')])),
                ('active', models.BooleanField(default=True)),
                ('member', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('teamgroup', models.ForeignKey(to='teamgroups.TeamGroup')),
            ],
        ),
        migrations.AddField(
            model_name='teamgroup',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='teamgroups.TeamGroupMembership'),
        ),
    ]
