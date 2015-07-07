from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Promotion, TariffPlan, Product, SKU, Offer


class PromotionSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField()
    process_segmentation_display = serializers.SerializerMethodField()
    tariff_plans = serializers.SlugRelatedField(
        many=True,
        slug_field='code',
        queryset=TariffPlan.objects.all()
    )

    class Meta:
        model = Promotion
        fields = ('name', 'description', 'code', 'contract_condition',
                  'agreement_length', 'process_segmentation',
                  'process_segmentation_display', 'market',
                  'offer_segmentation', 'is_active', 'activation_fee',
                  'sim_only', 'tariff_plans', 'links')

    def get_links(self, obj):
        request = self.context['request']
        links = {
            'self': reverse(
                'promotion-detail', kwargs={'code': obj.code}, request=request
            ),
            'tariff_plans': None
        }
        tariff_plans = [
            reverse('tariffplan-detail', kwargs={'code': t.code},
                    request=request) for t in obj.tariff_plans.all()
            ]

        if tariff_plans:
            links['tariff_plans'] = tariff_plans
        return links

    def get_process_segmentation_display(self, obj):
        display = obj.get_process_segmentation_display().split()
        return ', '.join(['%s' % ' '.join(item.split('_')) for item in display])


class TariffPlanSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = TariffPlan
        fields = ('name', 'description', 'code', 'monthly_fee', 'links')

    def get_links(self, obj):
        request = self.context['request']
        links = {
            'self': reverse(
                'tariffplan-detail', kwargs={'code': obj.code}, request=request
            ),
            'promotions': None
        }
        promotions = [
            reverse('promotion-detail', kwargs={'code': p.code},
                    request=request) for p in obj.promotions.all()
        ]
        if promotions:
            links['promotions'] = promotions
        return links


class ProductSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('model_name', 'manufacturer', 'full_name', 'product_type',
                  'links')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse(
                'product-detail', kwargs={'pk': obj.pk}, request=request
            )
        }


class SKUSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()
    product = serializers.SlugRelatedField(slug_field='full_name',
                                           queryset=Product.objects.all())

    class Meta:
        model = SKU
        fields = ('product', 'links', 'stock_code', 'color',
                  'availability', 'photo')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse(
                'sku-detail', kwargs={'stock_code': obj.stock_code},
                request=request
            ),
            'product': reverse(
                'product-detail', kwargs={'pk': obj.product_id}, request=request
            )
        }


class OfferSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()
    sku = serializers.SlugRelatedField(
        slug_field='stock_code', required=False, queryset=SKU.objects.all(),
        allow_null=True
    )
    promotion = serializers.SlugRelatedField(
        slug_field='code', queryset=Promotion.objects.filter(is_active=True))
    tariff_plan = serializers.SlugRelatedField(
        slug_field='code', queryset=TariffPlan.objects.all())
    sim_only = serializers.SerializerMethodField()
    monthly_fee = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ('sku', 'promotion', 'tariff_plan', 'price', 'sim_only',
                  'priority', 'product_page', 'crc_id', 'links', 'monthly_fee')

    def get_links(self, obj):
        request = self.context['request']
        links = {
            'self': reverse('offer-detail', kwargs={'crc_id': str(obj.crc_id)},
                            request=request),
            'sku': None,
            'promotion': reverse('promotion-detail',
                                 kwargs={'code': obj.promotion.code},
                                 request=request),
            'tariff_plan': reverse('tariffplan-detail',
                                   kwargs={'code': obj.tariff_plan.code},
                                   request=request),
        }
        if obj.sku:
            links['sku'] = reverse('sku-detail',
                                   kwargs={'stock_code': obj.sku.stock_code},
                                   request=request)
        return links

    def get_sim_only(self, obj):
        return obj.promotion.sim_only

    def get_monthly_fee(self, obj):
        return obj.tariff_plan.monthly_fee