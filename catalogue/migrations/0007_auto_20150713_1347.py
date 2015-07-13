# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0006_promotion_is_smartdom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='product_page',
            field=models.URLField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='process_segmentation',
            field=models.CharField(choices=[('IND.NEW.POSTPAID.ACQ', 'Abonament Nowy_numer'), ('IND.NEW.POSTPAID.MNP', 'Abonament Przenieś_numer'), ('IND.NEW.MIX.ACQ', 'MIX Nowy_numer'), ('IND.SUB.MIG.POSTPAID', 'Abonament Przejdź_na_abonament'), ('IND.SUB.MIG.MIX', 'MIX Przejdź_na_MIX'), ('IND.SUB.RET.POSTPAID', 'Abonament Przedłuż_umowę'), ('IND.SUB.RET.MIX', 'MIX Przedłuż_umowę'), ('IND.SUB.SAT.POSTPAID', 'Abonament Dokup_usługę Nowy_numer'), ('SOHO.NEW.POSTPAID.ACQ', 'Dla_firm Abonament Nowy_numer'), ('SOHO.NEW.POSTPAID.MNP', 'Dla_firm Abonament Przenieś_numer'), ('SOHO.SUB.SAT.POSTPAID', 'Dla_firm Abonament Dokup_usługę Nowy_numer'), ('SOHO.SUB.RET.POSTPAID', 'Dla_firm Abonamet Przedłuż_umowę')], max_length=50),
        ),
        migrations.AlterField(
            model_name='sku',
            name='stock_code',
            field=models.SlugField(unique=True, max_length=255),
        ),
    ]
