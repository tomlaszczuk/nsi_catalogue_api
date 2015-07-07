from rest_framework import authentication, permissions, viewsets

from .models import Promotion, TariffPlan, Product, SKU, Offer
from .serializers import (PromotionSerializer, TariffPlanSerializer,
                          ProductSerializer, SKUSerializer, OfferSerializer)


class DefaultsMixin(object):
    """
    Default settings for pagination
    """
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100


class PromotionViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoints for listing and creating promotions
    """
    queryset = Promotion.objects.order_by('is_active')
    serializer_class = PromotionSerializer
    lookup_field = 'code'
    lookup_url_kwarg = 'code'


class TariffPlanViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoints for listing and creating tariffplans
    """
    queryset = TariffPlan.objects.all()
    serializer_class = TariffPlanSerializer
    lookup_field = 'code'
    lookup_url_kwarg = 'code'


class ProductViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoints for listing and creating products
    """
    queryset = Product.objects.order_by('full_name')
    serializer_class = ProductSerializer


class SKUViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoints for listing and creating SKUs
    """
    queryset = SKU.objects.order_by('stock_code').prefetch_related('product')
    serializer_class = SKUSerializer
    lookup_url_kwarg = 'stock_code'
    lookup_field = 'stock_code'


class OfferViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoints for listing and creating Offers
    """
    queryset = Offer.objects.all().prefetch_related(
        'promotion', 'tariff_plan', 'sku'
    )
    serializer_class = OfferSerializer
    lookup_url_kwarg = 'crc_id'
    lookup_field = 'crc_id'