# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def _extract_year(year_list):
    for elem in year_list:
        if elem.isdigit():
            return int(elem)


def _concat_regeste(regeste_tokens):
    regeste = ''
    # for t in regeste_tokens:
    #     regeste += t
    # return regeste
    return '\n'.join(regeste_tokens)


def _extract_ruling_id(ruling_id_string):
    print(type(ruling_id_string))
    print(ruling_id_string)
    bge_nb, volume, ruling_nb = ruling_id_string.split(' ')

    ruling_id_dict = {
        'bge_nb': int(bge_nb),
        'volume': volume,
        'ruling_nb': int(ruling_nb)
    }
    return ruling_id_dict


class RulingItem(scrapy.Item):
    year = scrapy.Field(
        input_processor=_extract_year
    )
    ruling_id = scrapy.Field(
        input_processor=MapCompose(_extract_ruling_id),
        output_processor=TakeFirst()
    )
    regeste = scrapy.Field(
        input_processor=_concat_regeste,
        output_processor=TakeFirst()
    )
    pass
