from django.db import IntegrityError

from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from .models import Promotion, TariffPlan, Product, SKU, Offer


class PromotionSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField()
    process_segmentation_display = serializers.SerializerMethodField()
    tariff_plans = serializers.SlugRelatedField(
        many=True,
        slug_field='code',
        queryset=TariffPlan.objects.all()
    )
    code = serializers.CharField(
        validators=[UniqueValidator(queryset=Promotion.objects.all(),
                                    message="Promotion code must be unique")]
    )
    is_active = serializers.BooleanField()
    sim_only = serializers.BooleanField()
    is_smartdom = serializers.BooleanField()

    class Meta:
        model = Promotion
        fields = ('id', 'name', 'description', 'code', 'contract_condition',
                  'agreement_length', 'process_segmentation',
                  'process_segmentation_display', 'market',
                  'offer_segmentation', 'is_active', 'is_smartdom',
                  'activation_fee', 'sim_only', 'tariff_plans', 'links')

    def get_links(self, obj):
        request = self.context['request']
        links = {
            'self': reverse(
                'promotion-detail', kwargs={'code': obj.code}, request=request
            ),
            'tariff_plans': None,
            'offers': reverse(
                'offer-list', request=request
            ) + '?promotion={}'.format(obj.code)
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
    code = serializers.CharField(
        validators=[UniqueValidator(queryset=TariffPlan.objects.all(),
                                    message="Tariff code must be unique")]
    )

    class Meta:
        model = TariffPlan
        fields = ('id', 'name', 'description', 'code', 'monthly_fee', 'links')

    def get_links(self, obj):
        request = self.context['request']
        links = {
            'self': reverse(
                'tariffplan-detail', kwargs={'code': obj.code}, request=request
            ),
            'promotions': None,
            'offers': reverse(
                'offer-list', request=request
            ) + '?tariff_plan={}'.format(obj.code)
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
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'model_name', 'manufacturer', 'full_name',
                  'product_type', 'links')
        validators = [UniqueTogetherValidator(
            queryset=Product.objects.all(),
            fields=('model_name', 'manufacturer'),
            message="Combination of manufacturer and model name must be unique"
        )]

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse(
                'product-detail', kwargs={'pk': obj.pk}, request=request
            ),
            'skus': reverse(
                'sku-list', request=request) + '?product={}'.format(obj.id)
        }


class SKUSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()
    product = serializers.SlugRelatedField(slug_field='full_name',
                                           queryset=Product.objects.all())
    stock_code = serializers.CharField(
        validators=[UniqueValidator(queryset=SKU.objects.all(),
                                    message="Stock code must be unique")]
    )

    class Meta:
        model = SKU
        fields = ('id', 'product', 'links', 'stock_code', 'color',
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
            ),
            'offers': reverse(
                'offer-list', request=request
            ) + '?sku={}'.format(obj.stock_code)
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
    product_page = serializers.URLField(read_only=True)
    crc_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Offer
        fields = ('id', 'sku', 'promotion', 'tariff_plan', 'price', 'sim_only',
                  'priority', 'product_page', 'crc_id', 'links', 'monthly_fee')

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

    def get_monthly_fee(self, obj):
        return obj.tariff_plan.monthly_fee

    def save(self, **kwargs):
        try:
            super(OfferSerializer, self).save(**kwargs)
        except IntegrityError:
            raise serializers.ValidationError("Offer already exists")

    def validate(self, attrs):
        promotion = attrs.get('promotion')
        tariff_plan = attrs.get('tariff_plan')
        sku = attrs.get('sku')
        sim_only = Promotion.objects.get(code=promotion).sim_only
        promotion_instance = Promotion.objects.get(code=promotion)
        tariff_plan_instance = TariffPlan.objects.get(code=tariff_plan)
        tariffs_in_promotion = promotion_instance.tariff_plans.all()
        if tariff_plan_instance not in tariffs_in_promotion:
            raise serializers.ValidationError(
                "Tariffplan doesn not belong to Promotion"
            )
        if sku and sim_only:
            raise serializers.ValidationError(
                "You can't assign sku for sim only promotion"
            )
        elif not sku and not sim_only:
            raise serializers.ValidationError(
                "You can't assign no sku for non-sim-only promotion"
            )
        return attrs