# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0007_auto_20150713_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sku',
            name='stock_code',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
