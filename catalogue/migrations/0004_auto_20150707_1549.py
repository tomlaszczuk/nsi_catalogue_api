# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_auto_20150707_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='crc_id',
            field=models.BigIntegerField(null=True, blank=True, unique=True),
        ),
    ]
