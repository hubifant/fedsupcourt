# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst
from abc import ABC, abstractmethod


def _create_url(raw_url):
    return 'https://www.admin.ch/' + raw_url


class _HierarchicalIndex(Item, ABC):
    @abstractmethod
    def level_raw(self):
        pass
    # level = Field()


class CategoryItem(Item):
    hierarchy_level = Field(
        output_processor=TakeFirst()
    )
    id = Field(
        output_processor=TakeFirst()
    )
    name = Field(
        output_processor=TakeFirst()
    )
    parent = Field(
        output_processor=TakeFirst()
    )
    children = Field()
    url = Field()