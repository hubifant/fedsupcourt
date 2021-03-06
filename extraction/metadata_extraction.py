# -*- coding: utf-8 -*-

from datetime import datetime
import calendar
import locale
import re
import logging


class MetadataExtractor(object):

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

    # for extracting the responsible department of the Federal Supreme Court
    department_extraction_patterns = {
        'de': r'(?:(?<=Urteil de\w )|(?<=Entscheid de\w )|(?<=Verfügung de\w )|(?<=Beschluss de\w )|(?<=Präsidenten de\w))'  # before dep
              r'.*?\w'                                                                                 # dep name
              r'(?= i\.\s?S\.?| in Sachen| in S\.| (?:\w{3}\s?)?\d{1,2})',                             # after dep
        'fr': r'(?:(?<=arrêt de )|(?<=arrêt rendu par ))'
              r'.*?\w'
              r'(?= (?:dans|en) (?:la cause|les causes)| (?:du|le)?\s?\d{1,2}[^r]|,)',
        'it': r'(?<=della )(?!sentenza|decisione)'
              r'.*?\w'
              r'(?= nell[ae]| sul ricorso|z in re| (?:del(?:la|l\')?\s?)?\d{1,2}|, du)',
        'rr': r'(?<=sentenzia da la )'
              r'.*?\w'
              r'(?= concernent il cas)'
    }

    department_tagging_patterns = {
        'Administrative Law': r'(?:(?:schätzungs|verwaltungs|rekurs)kommission'
                              r'|verwaltungsrechtlich'
                              r'|administratif'
                              r'|amministrativo)',
        'Private Law': r'(präsident\w* des bundesgerichts'
                       r'|z[il]v[il]l(?!.*staats(?:recht|gericht))|'
                       r'c[il]v[il]le?(?!.*droit public))',
        'Public Law': r'(?:staats(?:recht|gericht)'
                      r'|instruktionsrichter'
                      r'|öffentlich'
                      r'|oera'
                      r'|public'
                      r'|pubblico)',
        'Criminal Law': r'(?:an(?:ge)?klagekammer|straf(?:recht|gericht)|accusa|p[eé]nale?'
                        r'|kassat[il]on|cassation|cassazione)'
                        r'(?!.*(?:staatsrecht|droit public))',
        'Debt Recovery and Bankruptcy': r'(?:schuldbetreibung|faillite|fallimenti)',
        'Social Insurance Law': r'(?:sozialrecht|versicherung|droit social|diritto sociale)'
    }

    # type of proceeding: in title of judgement; starts with '(', ends with ')' and does not contain any '(...)'
    type_of_proceeding_pattern = r'(?<=\().*?(?!.*\(.*\))(?=\))'

    # tokens for separating parties (also used for detecting the ruling's language)
    party_separator = {
        'de': {
            'start': r'(?:i\.?\s?S\.?|in Sachen|in S\.)\s?',
            'end': r' gegen '
        },
        'fr': {
            'start': r'(?:dans|en|contre) (?:l[ae] cause|les causes|l\'affaire) ',
            'end': r' contre '
        },
        'it': {
            'start': r'(?:nell[ae] caus[ae]|nella pratica|su[li]? ricors[oi]|in re) ',
            'end': r' contro '
        },
        'rr': {
            'start': r'concernent il cas ',
            'end': r' cunter '
        }
    }
    end_party_pattern = r'%s.*?'                        # starts after a party_separator (see above)
    end_party_pattern += r'(?:[^A-Z](?=\.\s?(?:\n|$))'  # if end of the sentence: don't include '.'
    end_party_pattern += r'|[A-Z]\.(?=\n|$)'            # if ending with abbr: include '.'
    end_party_pattern += r'|(?= \([^()]+\)(?:\n|$))'    # if ending with '(...)', don't include it (= proceeding type)
    end_party_pattern += r'|(?=\n|$))'                  # stop at newline at latest.

    def extract(self, item):
        if 'title_of_judgement' in item:
            url = item['url']
            extracted_date = self._extract_date(item['title_of_judgement'], url)
            if extracted_date is not None:
                item['date'] = extracted_date
            extracted_dossier_number = self._extract_dossier_number(item['title_of_judgement'], url)
            if extracted_dossier_number is not None:
                item['dossier_number'] = extracted_dossier_number
            extracted_department = self._extract_department(item['title_of_judgement'], url)
            if extracted_department is not None:
                item['department'] = extracted_department
            extracted_parties = self._extract_involved_parties(item['title_of_judgement'], url)
            if extracted_parties is not None:
                item['involved_parties'] = extracted_parties
            extracted_language = self._extract_language(item['title_of_judgement'], url)
            if extracted_language is not None:
                item['language'] = extracted_language
            extracted_type_of_proceeding = self._extract_type_of_proceeding(item['title_of_judgement'], url)
            if extracted_type_of_proceeding is not None:
                item['type_of_proceeding'] = extracted_type_of_proceeding
        return item

    def _extract_date(self, title_of_judgement, url):

        # first, try to match the date in the title of judgement
        date_match = re.search(self.date_pattern, title_of_judgement)

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
                date = datetime(year, 1, 1)
            else:
                date = datetime(year, month, day)
            return date

        logging.warning('Could not extract date. \nRuling: ' + url)

    def _extract_involved_parties(self, raw_parties, url):
        # extract claimant and defendant
        for language, separator in self.party_separator.items():
            start_claimant_match = re.search(separator['start'], raw_parties)

            # if claimant indicator has been found...
            if start_claimant_match is not None:
                start_claimant = start_claimant_match.span()[1]

                end_claimant_pattern = re.search(separator['end'], raw_parties)

                # if claimant and defendant can be separated...
                if end_claimant_pattern is not None:
                    end_claimant = end_claimant_pattern.span()[0]

                    # use end_party_pattern for extracting defendant
                    defendant = re.search(self.end_party_pattern % separator['end'], raw_parties).group()
                    defendant = re.sub(separator['end'], '', defendant)
                    parties = {
                        'claimant': raw_parties[start_claimant:end_claimant],
                        'defendant': defendant
                    }

                # otherwise there is only a claimant.
                else:
                    # use end_party_pattern for extracting claimant
                    claimant = re.search(self.end_party_pattern % separator['start'], raw_parties).group()
                    claimant = re.sub(separator['start'], '', claimant)
                    parties = {'claimant': claimant}

                return parties

        logging.warning('Could not extract parties. \nRuling: ' + url)

    def _extract_dossier_number(self, raw_dossier_number, url):
        # extract 'Dossiernummer' (e.g. '5A_153/2009' or '4C.197/2003')
        # http://www.bger.ch/uebersicht_numm_dossiers_internet_d_ab_2007.pdf
        dnb_match = re.search('\d+\w+[\_\.]\d+\/\d{4}', raw_dossier_number)

        if dnb_match is not None:
            return dnb_match.group()
        # logging.warning('Could not extract dossier number. \nRuling: ' + url)

    def _extract_department(self, raw_department, url):
        # extract the responsible department if possible.
        for language, department_pattern in self.department_extraction_patterns.items():
            department_match = re.search(department_pattern, raw_department, re.IGNORECASE)
            if department_match is not None:
                extracted_department = department_match.group()

                # try to tag the extracted department
                for department_tag, tagging_pattern in self.department_tagging_patterns.items():
                    if re.search(tagging_pattern, extracted_department, re.IGNORECASE) is not None:
                        return {'extracted_department': extracted_department, 'tag': department_tag}

                # if we arrive here, department could not be tagged. This is serious as tagging pattern must be adapted.
                logging.error('Could not tag the department "%s". The tagging pattern must be adapted!'
                              % extracted_department)

        logging.warning('Could not extract responsible department. \nRuling: ' + url)

    def _extract_type_of_proceeding(self, raw_type_of_proceeding, url):
        proceeding_match = re.search(self.type_of_proceeding_pattern, raw_type_of_proceeding)
        if proceeding_match is not None:
            return proceeding_match.group()
        # logging.warning('Could not extract the type of the proceeding. \nRuling: ' + url)

    def _extract_language(self, raw_parties, url):
        # language can be extracted if claimant and defendant can be extracted
        for language, separator in self.party_separator.items():
            start_claimant = re.search(separator['start'], raw_parties)

            # if claimant and defendant can be separated, language is known.
            if start_claimant is not None:
                return language

        logging.warning('Could not extract language. \nRuling: ' + url)
