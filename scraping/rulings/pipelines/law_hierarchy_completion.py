# -*- coding: utf-8 -*-

import calendar
import locale
import re
import logging
from scraping.rulings.items import LawItem


class LawHierarchyCompletionPipeline(object):

    # get lists of month names in german, french and italian.
    # names are normalised: lower case + accents removed
    locale.setlocale(locale.LC_ALL, 'de_CH.utf8')  # todo: make sure that locale exists!
    months_de = [m.lower() for m in calendar.month_name]
    locale.setlocale(locale.LC_ALL, 'fr_CH.utf8')
    months_fr = [m.lower().replace('é', 'e').replace('û', 'u') for m in calendar.month_name]
    locale.setlocale(locale.LC_ALL, 'it_CH.utf8')
    months_it = [m.lower() for m in calendar.month_name]
    locale.setlocale(locale.LC_ALL, 'C')
    months_rr = ['', 'schaner', 'favrer', 'mars', 'avrigl', 'matg', 'zercladur', 'fanadur', 'avust', 'settember', 'october',
                 'november', 'december']

    date_pattern = r'\b\d{1,2}(?:\.\s?|\s?er |o | da | )(?:\d{1,2}(?:\.\s?| )|\w+ )\d{4}'

    def process_item(self, item, spider):
        if 'id' not in item or 'url' not in item:
            logging.error('No ID or URL was extracted for item: ' + str(item))
        else:
            url = item['url']
            id = item['id']

            if 'name' in item:
                if type(item) is LawItem:
                    date = self._extract_enactment_date(item['name'], id, url)
                    if date is not None:
                        item['enactment_date'] = date
                        print(item['enactment_date'])

                    name, references, url_corrected = self._extract_references(item['name'], id, url)
                    if references is not None:
                        item['name'] = name
                        item['references'] = references
                        item['url'] = url_corrected
            else:
                logging.warning('No name was extracted for law ' + id + '\nLink: '+ url)
            return item

    def _extract_references(self, law_name, id, url):
        name = re.search(r'[^→]*', law_name).group()
        if '→' in law_name:
            references_raw = re.findall(r'(?<=→)(?:[^→]*)', law_name)

            references = []
            for ref_raw in references_raw:
                if 'art.' in ref_raw.lower():
                    ref = {'law_id': re.search(r'.*?(?=art.|$)', ref_raw, re.IGNORECASE).group(),
                           'article': re.search(r'art.*$', ref_raw, re.IGNORECASE).group()}
                else:
                    ref = {'law_id': ref_raw}
                references.append(ref)

            # if the law just contains references, the extracted url is pointing to the first reference
            print(url)
            url_corrected = re.sub('0.\d{2}.html#.*$', id[:4] + '.html#' + id, url)
            print(url_corrected)
            print()

            return name, references, url_corrected
        else:
            logging.info('Could not extract references. \nLaw ' + id + ': ' + url)
            return name, None, url

    def _extract_enactment_date(self, law_name, id, url):

        # first, try to match the date in the title of judgement
        date_match = re.search(self.date_pattern, law_name)

        if date_match is not None:
            raw_date = date_match.group()

            # simplify date splitting by removing 'da ' (if title of judgement is in Rhaeto-Romance)
            # --> relevancy.bger.ch/php/clir/http/index.php?lang=de&zoom=&type=show_document&highlight_docid=atf%3A%2F%2F139-II-145%3Ade
            raw_date = raw_date.replace(' da ', ' ')

            # match 4-digit number at the end of the string
            year_match = re.search(r'\d{4}$', raw_date)
            year = int(year_match.group())

            # match number at the beginning of the string:
            day_match = re.search(r'^\d+', raw_date)
            day = int(day_match.group())

            # extract month
            month_raw = re.search(r'(?<=\.| )(?:\d{1,2}|\w+)', raw_date).group()
            month = None

            # if month is represented as digit, we're done
            if month_raw.isdigit():
                month = int(month_raw)
            # if month is represented as string, we need to find out, which month it is (german, french and italian)
            else:
                month_raw = month_raw.lower()

                # if it's french, remove accents
                month_raw = month_raw.replace('é', 'e').replace('û', 'u')

                if month_raw in self.months_de:
                    month = self.months_de.index(month_raw)
                elif month_raw in self.months_fr:
                    month = self.months_fr.index(month_raw)
                elif month_raw in self.months_it:
                    month = self.months_it.index(month_raw)
                elif month_raw in self.months_rr:
                    month = self.months_rr.index(month_raw)

            if month is None:
                logging.warning("Could not extract month from '" + month_raw + "'. \nRuling: " + url)
                # date = datetime(year, 1, 1)
                date = str(year)
            else:
                # date = datetime(year, month, day)
                date = '%02d.%02d.%04d' % (day, month, year)
            return date

        logging.info('Could not extract date. \nLaw ' + id + ': ' + url)
