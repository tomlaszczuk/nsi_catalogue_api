# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0004_auto_20150707_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='is_active',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='sim_only',
            field=models.BooleanField(),
        ),
    ]
