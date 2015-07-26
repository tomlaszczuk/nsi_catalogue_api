import os

from django.core.management.base import BaseCommand
from django.conf import settings

from lxml import etree

from ._helpers import create_cheapest_entry, create_root_elem, add_time_stamp

from catalogue.models import Offer


class Command(BaseCommand):
    help = '''Create a xml dump of product catalogue containing only cheapest
    products in segmentation'''

    def handle(self, *args, **options):
        root = create_root_elem('products')
        add_time_stamp(root)
        offers = Offer.the_cheapest_offers()
        for offer in offers:
            root.append(create_cheapest_entry(offer))
        xml_str = etree.tostring(root, pretty_print=True, encoding='utf-8')
        with open(
                os.path.join(settings.XML_FEED_DIR, 'cheapest.xml'), 'wb'
        ) as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(xml_str)