# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('price', models.FloatField(null=True, default=None, blank=True)),
                ('priority', models.IntegerField(default=1)),
                ('crc_id', models.IntegerField(null=True, default=None, blank=True)),
                ('product_page', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('model_name', models.CharField(max_length=100)),
                ('manufacturer', models.CharField(max_length=50)),
                ('product_type', models.CharField(choices=[('PHONE', 'Telefon'), ('MODEM', 'Modem/Router'), ('SIM_CARD', 'Starter'), ('RETAIL', 'Konsola'), ('BUNDLE', 'Zestaw'), ('TAB', 'Tablet/Laptop')], max_length=20, default='PHONE')),
                ('full_name', models.CharField(max_length=150, default='', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, default='', blank=True)),
                ('description', models.CharField(max_length=255, default='', blank=True)),
                ('code', models.CharField(unique=True, max_length=10)),
                ('contract_condition', models.CharField(max_length=3, default='24A')),
                ('agreement_length', models.IntegerField(default=24)),
                ('process_segmentation', models.CharField(choices=[('IND.NEW.POSTPAID.ACQ', 'Abonament Nowy_numer'), ('IND.NEW.POSTPADI.MNP', 'Abonament Przenieś_numer'), ('IND.NEW.MIX.ACQ', 'MIX Nowy_numer'), ('IND.SUB.MIG.POSTPAID', 'Abonament Przejdź_na_abonament'), ('IND.SUB.MIG.MIX', 'MIX Przejdź_na_MIX'), ('IND.SUB.RET.POSTPAID', 'Abonament Przedłuż_umowę'), ('IND.SUB.RET.MIX', 'MIX Przedłuż_umowę'), ('IND.SUB.SAT.POSTPAID', 'Abonament Dokup_usługę Nowy_numer'), ('SOHO.NEW.POSTPAID.ACQ', 'Dla_firm Abonament Nowy_numer'), ('SOHO.NEW.POSTPAID.MNP', 'Dla_firm Abonament Przenieś_numer'), ('SOHO.SUB.SAT.POSTPAID', 'Dla_firm Abonament Dokup_usługę Nowy_numer'), ('SOHO.SUB.RET.POSTPAID', 'Dla_firm Abonamet Przedłuż_umowę')], max_length=50)),
                ('market', models.CharField(max_length=5, default='', blank=True)),
                ('offer_segmentation', models.CharField(max_length=100, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('activation_fee', models.FloatField(null=True, default=None, blank=True)),
                ('sim_only', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SKU',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('stock_code', models.SlugField(unique=True)),
                ('color', models.CharField(max_length=50, default='', blank=True)),
                ('availability', models.CharField(choices=[('AVAILABLE', 'Dostępny'), ('RUNNING_OUT', 'Kończy się'), ('NOT_AVAILABLE', 'Nie dostępny')], max_length=30)),
                ('photo', models.URLField(blank=True)),
                ('product', models.ForeignKey(related_name='skus', to='catalogue.Product')),
            ],
        ),
        migrations.CreateModel(
            name='TariffPlan',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, default='', blank=True)),
                ('description', models.CharField(max_length=255, default='', blank=True)),
                ('code', models.CharField(unique=True, max_length=10)),
                ('monthly_fee', models.FloatField()),
                ('promotions', models.ManyToManyField(related_name='tariff_plans', to='catalogue.Promotion', blank=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('model_name', 'manufacturer')]),
        ),
        migrations.AddField(
            model_name='offer',
            name='promotion',
            field=models.ForeignKey(related_name='offers', to='catalogue.Promotion'),
        ),
        migrations.AddField(
            model_name='offer',
            name='sku',
            field=models.ForeignKey(to='catalogue.SKU'),
        ),
        migrations.AddField(
            model_name='offer',
            name='tariff_plan',
            field=models.ForeignKey(related_name='offers', to='catalogue.TariffPlan'),
        ),
    ]
