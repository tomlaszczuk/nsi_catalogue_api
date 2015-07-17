# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0008_auto_20150713_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='old_price',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]
