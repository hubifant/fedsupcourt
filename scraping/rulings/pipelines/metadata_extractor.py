# -*- coding: utf-8 -*-

import calendar
import locale
import re
import warnings


class MetadataExtractorPipeline(object):

    # get lists of month names in german, french and italian.
    # names are normalised: lower case + accents removed
    locale.setlocale(locale.LC_ALL, 'de')
    months_de = [m.lower() for m in calendar.month_name]
    locale.setlocale(locale.LC_ALL, 'fr')
    months_fr = [m.lower().replace('é', 'e').replace('û', 'u') for m in calendar.month_name]
    locale.setlocale(locale.LC_ALL, 'it')
    months_it = [m.lower() for m in calendar.month_name]
    locale.setlocale(locale.LC_ALL, 'C')

    # departments of the Federal Supreme Court
    departments = {
        '1st Public Law Department': {
            'de': ['I. öffentlich-rechtliche Abteilung'],
            'fr': ['Iere Cour de Droit Public'],
            'it': ['I Corte di Diritto Pubblico']
        },
        '2nd Public Law Department': {
            'de': ['II. öffentlich-rechtliche Abteilung'],
            'fr': ['IIe Cour de Droit Public'],
            'it': ['I Corte di Diritto Pubblico']
        },
        '1st Civil Law Department': {
            'de': ['I. zivilrechtliche Abteilung'],
            'fr': ['Ie Cour de Droit Civil'],
            'it': ['I Corte di Diritto Civile']
        },
        '2nd Civil Law Department': {
            'de': ['II. zivilrechtliche Abteilung'],
            'fr': ['IIe Cour de Droit Civil'],
            'it': ['II Corte di Diritto Civile']
        },
        'Penal Law Department': {
            'de': ['strafrechtliche Abteilung', 'Kassationshof'],
            'fr': ['Cour de Droit Pénal', 'Cour de Cassation Pénale'],
            'it': ['Corte di Diritto Penale', 'Corte di Cassazione Penale']
        },
        '1st Social Law Department': {
            'de': ['I. sozialrechtliche Abteilung'],
            'fr': ['Ire Cour de Droit Social'],
            'it': ['I Corte di Diritto Sociale']
        },
        '2nd Social Law Department': {
            'de': ['II. sozialrechtliche Abteilung'],
            'fr': ['IIe Cour de Droit Social'],
            'it': ['II Corte di Diritto Sociale']
        }
    }

    # tokens for separating parties (also used for detecting the ruling's language)
    party_separator = {
        'de': {
            'start': 'i.S. ',
            'end': ' gegen '
        },
        'fr': {
            'start': 'dans la cause ',
            'end': ' contre '
        },
        'it': {
            'start': 'nella causa ',
            'end': ' contro '
        }
    }

    def process_item(self, item, spider):
        item['date'] = self._extract_date(item['title_of_judgement'])
        item['dossier_number'] = self._extract_dossier_number(item['title_of_judgement'])
        item['department'] = self._extract_department(item['title_of_judgement'])
        item['involved_parties'] = self._extract_involved_parties(item['title_of_judgement'])
        item['language'] = self._extract_language(item['title_of_judgement'])
        return item

    def _extract_date(self, raw_date):
        # match 4-digit number if preceded by '.' or ' '
        year_match = re.search(r'(?<=[\.\s])\d{4}', raw_date)

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

                if month_raw in self.months_de:
                    month = self.months_de.index(month_raw)
                elif month_raw in self.months_fr:
                    month = self.months_fr.index(month_raw)
                elif month_raw in self.months_it:
                    month = self.months_it.index(month_raw)

            if month is None:
                warnings.warn('Could not extract month.')
                # date = datetime(year, 1, 1)
                date = str(year)
            else:
                # date = datetime(year, month, day)
                date = '%02d.%02d.%04d' % (day, month, year)
            return date

    def _extract_involved_parties(self, raw_parties):
        # extract claimant and defendant
        for language, separator in self.party_separator.items():
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

    def _extract_dossier_number(self, raw_dossier_number):
        # extract 'Dossiernummer' (e.g. '5A_153/2009' or '4C.197/2003')
        # http://www.bger.ch/uebersicht_numm_dossiers_internet_d_ab_2007.pdf
        dnb_match = re.search('\d+\w+[\_\.]\d+\/\d{4}', raw_dossier_number)

        if dnb_match is not None:
            return dnb_match.group()

    def _extract_department(self, raw_department):
        # TODO: sometimes department is mentioned, sometimes chamber.
        # if the department name (in de, fr or it) occurs in the title of judgement, return the english department name
        for dep_en, department_translations in self.departments.items():
            for language, translations in department_translations.items():
                for translation in translations:
                    if translation.lower() in raw_department.lower():
                        return dep_en

    def _extract_language(self, raw_parties):
        # language can be extracted if claimant and defendant can be extracted
        for language, separator in self.party_separator.items():
            start_claimant = raw_parties.find(separator['start'])
            end_claimant = raw_parties.find(separator['end'])

            # if claimant and defendant can be separated, language is known.
            if start_claimant != -1 and end_claimant != -1:
                return language

        warnings.warn('Could not extract language.')