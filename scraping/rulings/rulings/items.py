# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


def _extract_year(year_list):
    for elem in year_list:
        if elem.isdigit():
            yield int(elem)


class IndexItem(scrapy.Item):
    links = scrapy.Field()


class VolumeItem(scrapy.Item):
    links = scrapy.Field()


class RulingsItem(scrapy.Item):
    year = scrapy.Field(
        input_processor=_extract_year
    )
    volume = scrapy.Field()
    bge_nr = scrapy.Field()
    ruling_nb = scrapy.Field()
    link = scrapy.Field()
    pass
