# -*- coding: utf-8 -*-

from lxml import etree
from lxml.etree import CDATA
from lxml import objectify

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
        return "0", "true"
    return "1", "false"


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
    monthly_fee = offer_ins.tariff_plan.monthly_fee
    if offer_ins.promotion.is_smartdom:
        if 'IND' in offer_ins.promotion.process_segmentation \
                and 'POSTPAID' in offer_ins.promotion.process_segmentation:
            monthly_fee -= 24.99
        else:
            monthly_fee /= 2
    if 'MIX' in segment:
        return "%.2f zł x %d" % (monthly_fee,
                                 offer_ins.promotion.agreement_length)
    elif 'SOHO' in segment:
        return "%.2f zł (%.2f zł z VAT)" % (
            monthly_fee,
            monthly_fee * 1.23
        )
    return "%.2f zł" % monthly_fee


def __modified_url(url):
    pass


def create_entry(offer_ins):
    product = etree.Element('product')
    product_id = __create_sub_element(product, 'id', str(offer_ins.crc_id))
    title = __create_sub_element(product, 'title')
    price = __create_sub_element(product, 'price', str(offer_ins.price))
    old_price = __create_sub_element(product, 'old_price',
                                     str(offer_ins.old_price))
    link = __create_sub_element(product, 'link', CDATA(offer_ins.product_page))
    thumb = __create_sub_element(product, 'thumb')
    status = __create_sub_element(product, 'status')
    __categorization(product, offer_ins)
    if offer_ins.sku:
        title.text = CDATA(offer_ins.sku.product.full_name)
        status.text = __interpret_availability(offer_ins.sku.availability)[0]
        thumb.text = offer_ins.sku.photo
    else:
        title.text = 'TYLKO SIM - %s' % offer_ins.promotion.code
        status.text = '1'
    custom = __create_sub_element(product, 'custom_1', __abo_price(offer_ins))
    return product


def __property(parent, attr, value):
    prop = __create_sub_element(parent, 'property', element_value=None,
                                attrib='name', attrib_value=attr)
    val = __create_sub_element(prop, 'value', value)
    return prop


def create_cheapest_entry(offer_ins):
    product = etree.Element('product')
    category = "%s-%s" % (
        offer_ins.promotion.process_segmentation.replace('.', '-'),
        offer_ins.sku.product.product_type
    )
    product.attrib['id'] = "%s-%s" % (
        offer_ins.sku.stock_code,
        category
    )
    name = __create_sub_element(product, 'name',
                                offer_ins.sku.product.full_name)
    price = __create_sub_element(product, 'price', str(offer_ins.price),
                                 'currency', 'PLN')
    nsi_url = __create_sub_element(product, 'NSI_URL', offer_ins.product_page)
    url = __create_sub_element(product, 'URL',
                               __modified_url(offer_ins.product_page))
    images = __create_sub_element(product, 'images')
    image = __create_sub_element(images, 'image', offer_ins.sku.photo)
    description = __create_sub_element(product, 'description', CDATA(''))
    properties = __create_sub_element(product, 'properties')
    __property(properties, 'manufacturer', offer_ins.sku.product.manufacturer)
    __property(properties, 'category', category)
    __property(properties, 'modified_url',
               __modified_url(offer_ins.product_page))
    __property(properties, 'country', 'Poland')
    __property(properties, 'deliveryCosts', '0.00')
    __property(properties, 'abo_price', str(offer_ins.tariff_plan.monthly_fee))
    __property(properties, 'available', offer_ins.sku.availability)
    __property(properties, 'available_for_order',
               __interpret_availability(offer_ins.sku.availability)[1])
    __property(properties, 'processSegmentationCode',
               offer_ins.promotion.process_segmentation)
    return product


def create_root_elem(name):
    return etree.Element(name)