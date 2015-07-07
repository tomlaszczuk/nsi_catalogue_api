from django.db import models


class Promotion(models.Model):

    SEGMENT_CHOICES = (
        ('Abonament Nowy_numer', 'IND.NEW.POSTPAID.ACQ'),
        ('Abonament Przenieś_numer', 'IND.NEW.POSTPADI.MNP'),
        ('MIX Nowy_numer', 'IND.NEW.MIX.ACQ'),
        ('Abonament Przejdź_na_abonament', 'IND.SUB.MIG.POSTPAID'),
        ('MIX Przejdź_na_MIX', 'IND.SUB.MIG.MIX'),
        ('Abonament Przedłuż_umowę', 'IND.SUB.RET.POSTPAID'),
        ('MIX Przedłuż_umowę', 'IND.SUB.RET.MIX'),
        ('Abonament Dokup_usługę Nowy_numer', 'IND.SUB.SAT.POSTPAID'),
        ('Dla_firm Abonament Nowy_numer', 'SOHO.NEW.POSTPAID.ACQ'),
        ('Dla_firm Abonament Przenieś_numer', 'SOHO.NEW.POSTPAID.MNP'),
        ('Dla_firm Abonament Dokup_usługę Nowy_numer', 'SOHO.SUB.SAT.POSTPAID'),
        ('Dla_firm Abonamet Przedłuż_umowę', 'SOHO.SUB.RET.POSTPAID')
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


class TariffPlan(models.Model):
    promotions = models.ManyToManyField(Promotion, related_name='tariff_plans',
                                        blank=True)
    name = models.CharField(max_length=100, blank=True, default='')
    description = models.CharField(max_length=255, blank=True, default='')
    code = models.CharField(max_length=10, unique=True)
    monthly_fee = models.FloatField()