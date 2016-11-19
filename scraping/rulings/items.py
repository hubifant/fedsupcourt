# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import calendar
from datetime import datetime
from html2text import HTML2Text
import locale
import re
import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
import warnings


# get lists of month names in german, french and italian.
# names are normalised: lower case + accents removed
locale.setlocale(locale.LC_ALL, 'de')
months_de = [m.lower() for m in calendar.month_name]
locale.setlocale(locale.LC_ALL, 'fr')
months_fr = [m.lower().replace('é', 'e').replace('û', 'u') for m in calendar.month_name]
locale.setlocale(locale.LC_ALL, 'it')
months_it = [m.lower() for m in calendar.month_name]
locale.setlocale(locale.LC_ALL, 'C')


# tokens for separating parties and detecting language
party_separator = {'de':
                       {'start': 'i.S. ',
                        'end': ' gegen '},
                   'fr':
                       {'start': 'dans la cause ',
                        'end': ' contre '},
                   'it':
                       {'start': 'nella causa ',
                        'end': ' contro '}
                   }

# init html2text class (make sure not to print random newlines and to ignore links):
html2text = HTML2Text()
html2text.body_width = 0
html2text.ignore_links = True

def _extract_date(raw_date):
    # match 4-digit number if preceded by '.' or ' '
    year_match = re.search(r'(?<=[\.,\s])\d{4}', raw_date)

    # if year was found, look for day and month
    if year_match is not None:
        year = int(year_match.group())

        # match one- or two-digit number preceded by ' ' and followed by '.' or ' '
        day_match = re.search('(?<=\s)\d{1,2}(?=[\.,\s])', raw_date)
        day = int(day_match.group())

        # extract month (digit between 1 and 12)
        # month token is between day and year token extracted above
        month_start = day_match.span()[1] + 1
        month_end = year_match.span()[0] - 1
        month_raw = raw_date[month_start:month_end].replace(' ', '').replace('.', '')
        month = None
        # if month is represented as digit, we're done
        if month_raw.isdigit():
            month = int(month_raw)
        # if month is represented as string, we need to find out, which month it is (german, french and italian)
        else:
            month_raw = month_raw.lower()

            # if it's french, remove accents
            month_raw = month_raw.replace('é', 'e').replace('û', 'u')

            if month_raw in months_de:
                month = months_de.index(month_raw)
            elif month_raw in months_fr:
                month = months_fr.index(month_raw)
            elif month_raw in months_it:
                month = months_it.index(month_raw)

        if month is None:
            warnings.warn('Could not extract month.')
            date = datetime(year, 1, 1)
            return date
        else:
            date = datetime(year, month, day)

        return date


def _extract_involved_parties(raw_parties):
    # extract claimant and defendant
    for language, separator in party_separator.items():
        start_claimant = raw_parties.find(separator['start'])
        end_claimant = raw_parties.find(separator['end'])

        # if claimant and defendant can be separated...
        if start_claimant != -1 and end_claimant != -1:
            start_claimant += len(separator['start'])
            start_defendant = end_claimant + len(separator['end'])

            # find the end of the defendant token (can end with '.' or '. (blabla)' or similarly)
            end_defendant = re.search(r'([\W\s]*)(\(.+\))?$', raw_parties).span()[0]
            parties = {
                'claimant': raw_parties[start_claimant:end_claimant],
                'defendant': raw_parties[start_defendant:end_defendant]
            }
            return parties

    warnings.warn('Could not extract parties.')


def _extract_language(raw_parties):
    # language can be extracted if claimant and defendant can be extracted
    for language, separator in party_separator.items():
        start_claimant = raw_parties.find(separator['start'])
        end_claimant = raw_parties.find(separator['end'])

        # if claimant and defendant can be separated, language is known.
        if start_claimant != -1 and end_claimant != -1:
            return language

    warnings.warn('Could not extract language.')


def _extract_ruling_id(ruling_id_string):
    # TODO: checking if number is correct. (throw exception?)
    """

    :param ruling_id_string: list containing one single string of format '123 I 4', where 123 is the bge_nb, I is volume and 4 the ruling_nb
    :return: dict containing bge_nb, volume and ruling_nb
    """
    # TODO replace 'mehr' with regexp?
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
    date = scrapy.Field(
        input_processor=MapCompose(_extract_date),
        output_processor=TakeFirst()
    )
    ruling_id = scrapy.Field(
        input_processor=MapCompose(_extract_ruling_id),
        output_processor=TakeFirst()
    )
    processing_number = scrapy.Field()
    involved_parties = scrapy.Field(
        input_processor=MapCompose(_extract_involved_parties),
        output_processor=TakeFirst()
    )
    language = scrapy.Field(
        input_processor=MapCompose(_extract_language),
        output_processor=TakeFirst()
    )
    rubrum = scrapy.Field(
        input_processor=MapCompose(filter_empty_a, html2text.handle),
        output_processor=''.join
    )
    regesta = scrapy.Field(
        input_processor=MapCompose(filter_empty_a, html2text.handle),
        output_processor=''.join
    )
    statement_of_affairs = scrapy.Field(
        input_processor=MapCompose(filter_empty_a, html2text.handle),
        output_processor=''.join
    )
    consideration = scrapy.Field(
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
