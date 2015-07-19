from django.core.management.base import BaseCommand

from lxml import etree

from ._helpers import create_cheapest_entry, create_root_elem

from catalogue.models import Offer


class Command(BaseCommand):
    help = '''Create a xml dump of product catalogue containing only cheapest
    products in segmentation'''

    def handle(self, *args, **options):
        root = create_root_elem('products')
        offers = Offer.the_cheapest_offers()
        for offer in offers:
            root.append(create_cheapest_entry(offer))
        xml_str = etree.tostring(root, pretty_print=True, encoding='utf-8')
        with open('second_test_file.xml', 'wb') as f:
            f.write(xml_str)