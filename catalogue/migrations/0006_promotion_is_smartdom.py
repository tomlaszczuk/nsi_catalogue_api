# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0005_auto_20150708_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='is_smartdom',
            field=models.BooleanField(default=False),
        ),
    ]
