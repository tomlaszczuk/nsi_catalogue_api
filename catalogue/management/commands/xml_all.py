import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from lxml import etree

from catalogue.models import Offer

from ._helpers import create_entry, create_root_elem


class Command(BaseCommand):
    help = "Creates a xml file with dump of whole product catalogue"

    def handle(self, *args, **options):
        offers = Offer.objects.filter(
            promotion__is_active=True).prefetch_related('sku', 'tariff_plan',
                                                        'promotion')
        root = create_root_elem('products')
        for offer in offers:
            root.append(create_entry(offer))
        xml_str = etree.tostring(root, pretty_print=True, encoding='utf-8')
        with open(os.path.join(settings.XML_FEED_DIR, 'all.xml'), 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(xml_str)