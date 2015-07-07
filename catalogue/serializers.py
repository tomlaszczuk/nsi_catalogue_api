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