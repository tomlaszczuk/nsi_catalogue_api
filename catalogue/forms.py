import django_filters

from .models import Offer, Product, SKU, Promotion, TariffPlan


class PromotionFilter(django_filters.FilterSet):

    class Meta:
        model = Promotion
        fields = ('is_active',)


class SKUFilter(django_filters.FilterSet):

    class Meta:
        model = SKU
        fields = ('product',)


class OfferFilter(django_filters.FilterSet):

    class Meta:
        model = Offer
        fields = ('tariff_plan', 'promotion', 'sku',)

    def __init__(self, *args, **kwargs):
        super(OfferFilter, self).__init__(*args, **kwargs)
        self.filters['sku'].extra.update({
            'to_field_name': 'stock_code'
        })
        self.filters['promotion'].extra.update({
            'to_field_name': 'code'
        })
        self.filters['tariff_plan'].extra.update({
            'to_field_name': 'code'
        })