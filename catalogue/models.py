# -*- coding: utf-8 -*-

from binascii import crc32

from django.db import models
from django.db.models import Min


class Promotion(models.Model):

    SEGMENT_CHOICES = (
        ('IND.NEW.POSTPAID.ACQ', 'Abonament Nowy_numer'),
        ('IND.NEW.POSTPAID.MNP', 'Abonament Przenieś_numer'),
        ('IND.NEW.MIX.ACQ', 'MIX Nowy_numer'),
        ('IND.SUB.MIG.POSTPAID', 'Abonament Przejdź_na_abonament'),
        ('IND.SUB.MIG.MIX', 'MIX Przejdź_na_MIX'),
        ('IND.SUB.RET.POSTPAID', 'Abonament Przedłuż_umowę'),
        ('IND.SUB.RET.MIX', 'MIX Przedłuż_umowę'),
        ('IND.SUB.SAT.POSTPAID', 'Abonament Dokup_usługę Nowy_numer'),
        ('SOHO.NEW.POSTPAID.ACQ', 'Dla_firm Abonament Nowy_numer'),
        ('SOHO.NEW.POSTPAID.MNP', 'Dla_firm Abonament Przenieś_numer'),
        ('SOHO.SUB.SAT.POSTPAID', 'Dla_firm Abonament Dokup_usługę Nowy_numer'),
        ('SOHO.SUB.RET.POSTPAID', 'Dla_firm Abonamet Przedłuż_umowę'),
    )

    name = models.CharField(max_length=100, blank=True, default='')
    description = models.CharField(max_length=255, blank=True, default='')
    code = models.CharField(max_length=10, unique=True)
    contract_condition = models.CharField(max_length=3, default='24A')
    agreement_length = models.IntegerField(default=24)
    process_segmentation = models.CharField(max_length=50,
                                            choices=SEGMENT_CHOICES)
    market = models.CharField(max_length=5, blank=True, default='')
    offer_segmentation = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField()
    activation_fee = models.FloatField(null=True, blank=True, default=None)
    sim_only = models.BooleanField()
    is_smartdom = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.market = self.process_segmentation.split('.')[0]
        super(Promotion, self).save(*args, **kwargs)

    def __str__(self):
        return self.code


class TariffPlan(models.Model):
    promotions = models.ManyToManyField(Promotion, related_name='tariff_plans',
                                        blank=True)
    name = models.CharField(max_length=100, blank=True, default='')
    description = models.CharField(max_length=255, blank=True, default='')
    code = models.CharField(max_length=10, unique=True)
    monthly_fee = models.FloatField()

    def __str__(self):
        return self.code


class Product(models.Model):

    PRODUCT_TYPE_CHOICES = (
        ('PHONE', 'Telefon'),
        ('MODEM', 'Modem/Router'),
        ('SIM_CARD', 'Starter'),
        ('RETAIL', 'Konsola'),
        ('BUNDLE', 'Zestaw'),
        ('TAB', 'Tablet/Laptop'),
    )

    model_name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=50)
    product_type = models.CharField(choices=PRODUCT_TYPE_CHOICES, max_length=20,
                                    default='PHONE')
    full_name = models.CharField(max_length=150, blank=True, default='')

    class Meta:
        unique_together = ('model_name', 'manufacturer')

    def save(self, *args, **kwargs):
        self.full_name = "{0} {1}".format(self.manufacturer, self.model_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name


class SKU(models.Model):

    AVAILABILITY_CHOICES = (
        ('AVAILABLE', 'Dostępny'),
        ('RUNNING_OUT', 'Kończy się'),
        ('NOT_AVAILABLE', 'Nie dostępny'),
    )

    product = models.ForeignKey(Product, related_name='skus')
    stock_code = models.CharField(unique=True, max_length=255)
    color = models.CharField(max_length=50, blank=True, default='')
    availability = models.CharField(max_length=30, choices=AVAILABILITY_CHOICES)
    photo = models.URLField(blank=True)

    def __str__(self):
        return self.stock_code


class Offer(models.Model):
    promotion = models.ForeignKey(Promotion, related_name='offers')
    tariff_plan = models.ForeignKey(TariffPlan, related_name='offers')
    sku = models.ForeignKey(SKU, blank=True, null=True, default=None)
    price = models.FloatField(blank=True, null=True, default=None)
    priority = models.IntegerField(default=1)
    crc_id = models.BigIntegerField(blank=True, null=True, unique=True)
    product_page = models.URLField(blank=True, max_length=500)
    old_price = models.FloatField(blank=True, null=True, default=None)

    def __str__(self):
        return str(self.crc_id)

    @staticmethod
    def generate_product_page_url(**kwargs):
        url = 'http://plus.pl/'
        if 'SOHO' in kwargs['processSegmentationCode']:
            url += 'dla-firm/'
        if kwargs['deviceTypeCode'] == 'TAB':
            url += 'tablet-laptop?'
        elif kwargs['deviceTypeCode'] == 'MODEM':
            url += 'modem-router?'
        else:
            url += 'telefon?'
        url += "&".join(["%s=%s" % (k, kwargs[k]) for k in kwargs])
        return url

    @staticmethod
    def generate_sim_only_shopping_flow_url(**kwargs):
        url = 'http://plus.pl/'
        if 'SOHO' in kwargs['processSegmentationCode']:
            url += 'dla-firm/'
        url += 'shopping-flow?'
        url += "&".join(["%s=%s" % (k, kwargs[k]) for k in kwargs])
        return url

    def generate_crc32_id(self):
        if not self.promotion.sim_only:
            data = "%s_%s_%s_%s" % (
                self.sku.stock_code, self.promotion.code,
                self.tariff_plan.code, self.promotion.contract_condition
            )
        else:
            data = "%s_%s_%s" % (
                self.promotion.code, self.tariff_plan.code,
                self.promotion.contract_condition
            )
        data = bytes(data, encoding='utf-8')
        return crc32(data) & 0xffffffff

    def save(self, *args, **kwargs):
        if self.promotion.sim_only:
            self.product_page = self.generate_sim_only_shopping_flow_url(
                offerNSICode=self.promotion.code,
                tariffPlanCode=self.tariff_plan.code,
                marketTypeCode=self.promotion.market,
                processSegmentationCode=self.promotion.process_segmentation,
                contractConditionCode=self.promotion.contract_condition
            )
        else:
            self.product_page = self.generate_product_page_url(
                deviceStockCode=self.sku.stock_code,
                deviceTypeCode=self.sku.product.product_type,
                offerNSICode=self.promotion.code,
                tariffPlanCode=self.tariff_plan.code,
                marketTypeCode=self.promotion.market,
                processSegmentationCode=self.promotion.process_segmentation,
                contractConditionCode=self.promotion.contract_condition
            )
        self.crc_id = self.generate_crc32_id()
        super(Offer, self).save(*args, **kwargs)

    @staticmethod
    def the_cheapest_offers():
        cheapest_offers = []
        products = Product.objects.all()
        segments = Promotion.SEGMENT_CHOICES
        all_offers = Offer.objects.all().prefetch_related(
            'promotion', 'sku', 'tariff_plan')
        for segment in segments:
            for product in products:
                min_price = all_offers.filter(
                    sku__product=product,
                    promotion__process_segmentation=segment[0]
                ).aggregate(Min('price'))['price__min']
                min_fee = all_offers.filter(
                    sku__product=product, price=min_price,
                    promotion__process_segmentation=segment[0]
                ).aggregate(Min('tariff_plan__monthly_fee'))
                min_monthly_fee = min_fee['tariff_plan__monthly_fee__min']
                offers = all_offers.filter(
                    sku__product=product,
                    tariff_plan__monthly_fee=min_monthly_fee,
                    promotion__process_segmentation=segment[0]
                )
                cheapest_offers.extend(offers)
        return cheapest_offers