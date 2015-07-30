# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teamgroups', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teamgroup',
            options={'permissions': (('view_teamgroup', 'Can view teamgroup'), ('leave_teamgroup', 'Can leave teamgroup'))},
        ),
    ]
