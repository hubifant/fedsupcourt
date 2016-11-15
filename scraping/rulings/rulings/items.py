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

def _concat_regeste(regeste_tokens):
    regeste = ''
    # for t in regeste_tokens:
    #     regeste += t
    # return regeste
    yield '\n'.join(regeste_tokens)


class RulingItem(scrapy.Item):
    year = scrapy.Field(
        input_processor=_extract_year
    )
    bge_nr = scrapy.Field()
    volume = scrapy.Field()
    ruling_nb = scrapy.Field()
    regeste = scrapy.Field(
        input_processor=_concat_regeste
    )
    pass
