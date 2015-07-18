from lxml import etree
from lxml.etree import CDATA

from catalogue.models import Promotion


def __create_sub_element(parent, name, element_value=None,
                         attrib=None, attrib_value=None):
    elem = etree.SubElement(parent, name)
    if element_value is not None:
        elem.text = element_value
    if attrib is not None and attrib_value is not None:
        elem.attrib[attrib] = attrib_value
    return elem


def __interpret_availability(availability):
    if 'NOT' in availability:
        return "0"
    return "1"


def __create_segment_dict():
    segment_dict = {}
    for index, item in enumerate(Promotion.SEGMENT_CHOICES):
        segment_dict[item[0]] = index + 3
    return segment_dict


def __categorization(parent, offer_ins):
    market = offer_ins.promotion.market
    market_id = '1' if market == 'IND' else '2'
    segment = offer_ins.promotion.process_segmentation
    segment_dict = __create_segment_dict()
    current_id = len(Promotion.SEGMENT_CHOICES) + 4
    if offer_ins.promotion.sim_only:
        service_type = (str(current_id), 'TYLKO SIM')
    else:
        device_type = offer_ins.sku.product.product_type
        service_type = (str(current_id+1), 'VOICE') if device_type == 'PHONE' \
            else (str(current_id+2), 'DATA')
    is_smartdom = offer_ins.promotion.is_smartdom
    is_smartdom_id = str(current_id+4) if is_smartdom else str(current_id+3)
    __create_sub_element(parent, 'category_1', market, 'id', market_id)
    __create_sub_element(parent, 'category_2', segment,
                         'id', str(segment_dict[segment]))
    __create_sub_element(parent, 'category_3', service_type[1],
                         'id', service_type[0])
    __create_sub_element(parent, 'category_4', str(is_smartdom),
                         'id', is_smartdom_id)


def __abo_price(offer_ins):
    segment = offer_ins.promotion.process_segmentation
    if 'MIX' in segment:
        return "%.2f zł x %d" % (offer_ins.tariff_plan.monthly_fee,
                                 offer_ins.promotion.agreement_length)
    elif 'SOHO' in segment:
        return "%.2f zł (%.2f zł z VAT)" % (
            offer_ins.tariff_plan.monthly_fee,
            offer_ins.tariff_plan.monthly_fee * 1.23
        )
    return "%.2f zł" % offer_ins.tariff_plan.monthly_fee


def create_entry(offer_ins):
    product = etree.Element('product')
    product_id = __create_sub_element(product, 'id', str(offer_ins.crc_id))
    title = __create_sub_element(product, 'title',
                                 CDATA(offer_ins.sku.product.full_name))
    price = __create_sub_element(product, 'price', str(offer_ins.price))
    old_price = __create_sub_element(product, 'old_price',
                                     str(offer_ins.old_price))
    link = __create_sub_element(product, 'link', CDATA(offer_ins.product_page))
    thumb = __create_sub_element(product, 'thumb', offer_ins.sku.photo)
    status = __create_sub_element(
        product, 'status', __interpret_availability(offer_ins.sku.availability)
    )
    __categorization(product, offer_ins)
    custom = __create_sub_element(product, 'custom_1', __abo_price(offer_ins))
    return product


def create_root_elem():
    root = etree.Element('products')
    return root