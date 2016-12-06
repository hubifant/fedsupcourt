# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst
import re


def _extract_subcat_name(raw_name):
    raw_name = re.sub(r'^.*?- ', '', raw_name, flags=re.DOTALL)
    return re.sub(r'[^\w]*$', '', raw_name, flags=re.DOTALL)


class _HierarchyItem(Item):
    hierarchy_level = Field(
        output_processor=TakeFirst()
    )
    id = Field(
        output_processor=TakeFirst()
    )
    name = Field(
        input_processor=MapCompose(_extract_subcat_name),
        output_processor=TakeFirst()
    )
    parent = Field(
        output_processor=TakeFirst()
    )
    url = Field(
        output_processor=TakeFirst()
    )
    is_law = Field()


class CategoryItem(_HierarchyItem):
    children = Field()


class LawItem(_HierarchyItem):
    references = Field()
