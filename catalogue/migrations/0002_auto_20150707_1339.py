# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='sku',
            field=models.ForeignKey(blank=True, null=True, default=None, to='catalogue.SKU'),
        ),
    ]
