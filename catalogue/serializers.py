from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Promotion, TariffPlan, Product, SKU, Offer


class PromotionSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField()
    process_segmentation_display = serializers.SerializerMethodField()

    class Meta:
        model = Promotion
        fields = ('name', 'description', 'code', 'contract_condition',
                  'agreement_length', 'process_segmentation',
                  'process_segmentation_display', 'market',
                  'offer_segmentation', 'is_active', 'activation_fee',
                  'sim_only', 'links')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse(
                'promotion-detail', kwargs={'code': obj.code}, request=request
            )
        }

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
        return {
            'self': reverse(
                'tariffplan-detail', kwargs={'code': obj.code}, request=request
            )
        }


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
    product = serializers.SlugRelatedField(
        slug_field=Product.full_name, required=False, read_only=True
    )

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
                'product_detail', kwargs={'pk': obj.product_id}, request=request
            )
        }


class OfferSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()
    sku = serializers.SlugRelatedField(
        slug_field=SKU.stock_code, required=False, read_only=True
    )
    promotion = serializers.SlugRelatedField(
        slug_field=Promotion.code, required=False, read_only=True
    )
    tariff_plan = serializers.SlugRelatedField(
        slug_field=TariffPlan.code, required=False, read_only=True
    )
    sim_only = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ('sku', 'promotion', 'tariff_plan', 'price', 'sim_only',
                  'priority', 'product_page', 'crc_id', 'links')

    def get_links(self, obj):
        request = self.context['request']
        links = {
            'self': reverse('offer-detail', kwargs={'crc_id': obj.crc_id},
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