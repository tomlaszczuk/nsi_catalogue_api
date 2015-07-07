from django.db import models


class Promotion(models.Model):

    SEGMENT_CHOICES = (
        ('IND.NEW.POSTPAID.ACQ', 'Abonament Nowy_numer'),
        ('IND.NEW.POSTPADI.MNP', 'Abonament Przenieś_numer'),
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
    is_active = models.BooleanField(default=True)
    activation_fee = models.FloatField(null=True, blank=True, default=None)
    sim_only = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.market = self.process_segmentation.split('.')[0]

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
        'PHONE', 'Telefon',
        'MODEM', 'Modem/Router',
        'SIM_CARD', 'Starter',
        'RETAIL', 'Konsola',
        'BUNDLE', 'Zestaw',
        'TAB', 'Tablet/Laptop'
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

    def __str__(self):
        return self.full_name


class SKU(models.Model):

    AVAILABILITY_CHOICES = (
        'Dostępny', 'AVAILABLE',
        'Kończy się', 'RUNNING_OUT',
        'Nie dostępny', 'NOT_AVAILABLE'
    )

    product = models.ForeignKey(Product, related_name='skus')
    stock_code = models.SlugField(unique=True)
    color = models.CharField(max_length=50, blank=True, default='')
    availability = models.CharField(max_length=30)
    photo = models.URLField(blank=True)

    def __str__(self):
        return self.stock_code