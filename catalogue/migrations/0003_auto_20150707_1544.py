# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_auto_20150707_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='crc_id',
            field=models.IntegerField(blank=True, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='product_page',
            field=models.URLField(blank=True),
        ),
    ]
