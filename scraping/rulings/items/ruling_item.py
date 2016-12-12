# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from html2text import HTML2Text
import re
import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


# init html2text class (make sure not to print random newlines and to ignore links):
html2text = HTML2Text()
html2text.body_width = 0  # make sure not to insert newlines every X letters
html2text.ignore_links = True  # links are represented as '(LINKTEXT)[URL]' if set to False; otherwise just 'LINKTEXT'


def _extract_ruling_id(ruling_id_string):
    """
    :param ruling_id_string: list containing one single string of format '123 I 4', where 123 is the bge_nb, I is volume and 4 the ruling_nb
    :return: dict containing bge_nb, volume and ruling_nb
    """
    if not 'mehr' in ruling_id_string:
        # ruling id can occur with u'\xa0'
        ruling_id_string = ruling_id_string.replace(u'\xa0', ' ')
        bge_nb, volume, ruling_nb = ruling_id_string.split(' ')

        ruling_id_dict = {
            'bge_nb': int(bge_nb),
            'volume': volume,
            'ruling_nb': int(ruling_nb)
        }
        return ruling_id_dict


def _extract_art_refs(raw_art_refs):
    # remove 'start token'
    start_token = 'Artikel:'
    more_token = 'mehr...'
    raw_art_refs = raw_art_refs.replace(start_token, '')
    raw_art_refs = raw_art_refs.replace(more_token, '')

    # remove newlines
    raw_art_refs = re.sub(r'\n', ' ', raw_art_refs)

    # remove double-spaces
    raw_art_refs = re.sub(r'\s{2,}', ' ', raw_art_refs)

    # remove spaces at beginning and end
    raw_art_refs = re.sub(r'^\s+', '', raw_art_refs)
    raw_art_refs = re.sub(r'\s+$', '', raw_art_refs)

    # split at each comma if followed by 'art' and return list
    return re.split(r'\,\s?(?=[aA]rt)', raw_art_refs)


def filter_empty_a(html_string):
    if re.search(r'^\<a[^\/]*name=\"idp\d+\"\><\/a>$', html_string) is None:
        return html_string


class RulingItem(scrapy.Item):
    _id = scrapy.Field(
        input_processor=MapCompose(_extract_ruling_id),
        output_processor=TakeFirst()
    )
    title_of_judgement = scrapy.Field(
        input_processor=MapCompose(filter_empty_a, html2text.handle),
        output_processor=''.join
    )
    core_issue = scrapy.Field(
        input_processor=MapCompose(filter_empty_a, html2text.handle),
        output_processor=''.join
    )
    statement_of_affairs = scrapy.Field(
        input_processor=MapCompose(filter_empty_a, html2text.handle),
        output_processor=''.join
    )
    paragraph = scrapy.Field(
        input_processor=MapCompose(filter_empty_a, html2text.handle),
        output_processor=''.join
    )
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    bge_refs = scrapy.Field(
        input_processor=MapCompose(_extract_ruling_id)
    )
    art_refs = scrapy.Field(
        input_processor=''.join,
        output_processor=MapCompose(_extract_art_refs)
    )

    # the following fields are extracted in the pipeline.
    date = scrapy.Field()
    dossier_number = scrapy.Field()
    department = scrapy.Field()
    type_of_proceeding = scrapy.Field()
    involved_parties = scrapy.Field()
    language = scrapy.Field()
    international_treaties = scrapy.Field()
    international_customary_law = scrapy.Field()
    international_law_in_general = scrapy.Field()
