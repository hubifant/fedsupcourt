# contains dummy scrapy item for testing purposes.

from datetime import datetime
from scraping.rulings import RulingItem

# case_incomplete: for testing a simple keyword extraction in the case where a ruling does not contain all 3 chapters
case_incomplete = {'input_item': RulingItem(), 'expected_output': RulingItem()}
case_incomplete['input_item']['core_issue'] = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam ' \
                                              'nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, ' \
                                              'sed diam voluptua. At vero eos et accusam et justo duo dolores et ea ' \
                                              'rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ' \
                                              'ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur ' \
                                              'sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et ' \
                                              'dolore magna aliquyam erat, "sed Abkommen". At vero eos et accusam et ' \
                                              'justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea ' \
                                              'takimata sanctus est Lorem ipsum dolor sit amet.'
case_incomplete['input_item']['paragraph'] = 'The chapter \'paragraph\' does not contain any keyword.'

case_incomplete['expected_output']['international_treaties'] = {
    'broad': {
        'contexts': [{
            'chapter': 'core_issue',
            'keyword': 'sed Abkommen',
            'sentence': 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt '
                        'ut labore et dolore magna aliquyam erat, "sed Abkommen".'
        }],
        'keywords': [{'keyword': 'sed Abkommen', 'count': 1}]
    }
}

# case_keyword_completeness: for testing if all expected keywords related with international treaties are extracted.
case_completeness_int_treaties = {'input_item': RulingItem(), 'expected_output': {}}
case_completeness_int_treaties['input_item']['core_issue'] = '''
    Völkerrechtliches Abkommen
    Völkerrechtliche Abkommen
    Völkerrechtlichen Abkommen
    Völkerrechtlichen Abkommens
    Völkerrechtlicher Abkommen
    Internationales Abkommen
    Internationale Abkommen
    Internationalen Abkommen
    Internationalen Abkommens
    Internationaler Abkommen
    Völkerrechtliches Übereinkommen
    Völkerrechtliche Übereinkommen
    Völkerrechtlichen Übereinkommen
    Völkerrechtlichen Übereinkommens
    Völkerrechtlicher Übereinkommen
    Internationales Übereinkommen
    Internationale Übereinkommen
    Internationalen Übereinkommen
    Internationalen Übereinkommens
    Internationaler Übereinkommen
    Übereinkommen
    Abkommen
    Völkerrechtlicher Vertrag
    Völkerrechtlichen Vertrags
    Völkerrechtlichen Vertrages
    Völkerrechtlichen Vertrag
    Völkerrechtliche Verträge
    Völkerrechtlichen Verträge
    Völkerrechtlicher Verträge
    Internationaler Vertrag
    Internationalen Vertrags
    Internationalen Vertrages
    Internationalen Vertrag
    Internationale Verträge
    Internationalen Verträge
    Internationaler Verträge
    Internationaler Pakt
    Internationalen Pakts
    Internationalen Paktes
    Internationalen Pakt
    Internationale Pakte
    Internationalen Pakte
    Internationaler Pakte
    Völkerrechtlicher Pakt
    Völkerrechtlichen Pakts
    Völkerrechtlichen Paktes
    Völkerrechtlichen Pakt
    Völkerrechtliche Pakte
    Völkerrechtlichen Pakte
    Völkerrechtlicher Pakte
    Pakt
    Pakte
    Pakts

    Traité international
    Traités internationaux
    Traité
    Traités
    Accord international
    Accords internationaux
    Accord
    Convention internationale
    Conventions internationales
    Convention
    Conventions
    Contrat international
    Contrats internationaux
    Pacte international
    Pactes internationaux
    Pacte
    Trattato internazionale
    Trattati internazionali
    Trattato di stato
    Trattati di stato
    Convenzione internazionale
    Convenzioni internazionali
    Accordo internazionale
    Accordi internazionali
    Patto internazionale
    Patti internazionali
    Patto
    Patti
    Internationales Vertragsrecht
    Internationale Vertragsrecht
    Internationalen Vertragesrecht
    Internationalen Vertragsrechts
    Internationalem Vertragsrecht
    Staatsvertrag
    Staatsverträge
    Staatsvertrags
    Staatsvertrages

    Convenzione tra la Svizzera e l'Italia
    Doppelbesteuerungsabkommen
    Doppelbesteuerungsabkommens
    accord pour la double crème
    convenzione sulla doppia imposizione
    pacte entre la Suisse et la France
    patto di non


    Ablösungsabkommen
    accord avec l'allemagne
    accordi italo-svizzeri
    diritto internazionale convenzionale


    staaten abkommen
    staaten vertragliche
    staaten vertragspartei
    staaten übereinkommen
    staatliche abkommen
    staatlichen abkommen
    staatlichen abkommens
    staatlichen vertragsrecht
    staatlichen verträgen
    staatlichen Übereinkommen
    staatlichen Übereinkommens
    staatlicher abkommen
    staatlicher vertrag
    staatliches abkommen
    staatsgebiet verträge

    droit international conventionnel
    droit international privé conventionnel
'''
case_completeness_int_treaties['expected_output']['clear'] = [
    'Völkerrechtliches Abkommen', 'Völkerrechtliche Abkommen', 'Völkerrechtlichen Abkommen',
    'Völkerrechtlichen Abkommens', 'Völkerrechtlicher Abkommen', 'Internationales Abkommen', 'Internationale Abkommen',
    'Internationalen Abkommen', 'Internationalen Abkommens', 'Internationaler Abkommen',
    'Völkerrechtliches Übereinkommen', 'Völkerrechtliche Übereinkommen', 'Völkerrechtlichen Übereinkommen',
    'Völkerrechtlichen Übereinkommens', 'Völkerrechtlicher Übereinkommen', 'Internationales Übereinkommen',
    'Internationale Übereinkommen', 'Internationalen Übereinkommen', 'Internationalen Übereinkommens',
    'Internationaler Übereinkommen',
    'Völkerrechtlicher Vertrag', 'Völkerrechtlichen Vertrags', 'Völkerrechtlichen Vertrages',
    'Völkerrechtlichen Vertrag', 'Völkerrechtliche Verträge', 'Völkerrechtlichen Verträge',
    'Völkerrechtlicher Verträge', 'Internationaler Vertrag', 'Internationalen Vertrags', 'Internationalen Vertrages',
    'Internationalen Vertrag', 'Internationale Verträge', 'Internationalen Verträge', 'Internationaler Verträge',
    'Internationaler Pakt', 'Internationalen Pakts', 'Internationalen Paktes', 'Internationalen Pakt',
    'Internationale Pakte', 'Internationalen Pakte', 'Internationaler Pakte', 'Völkerrechtlicher Pakt',
    'Völkerrechtlichen Pakts', 'Völkerrechtlichen Paktes', 'Völkerrechtlichen Pakt', 'Völkerrechtliche Pakte',
    'Völkerrechtlichen Pakte', 'Völkerrechtlicher Pakte',
    'Traité international', 'Traités internationaux', 'Accord international',
    'Accords internationaux', 'Convention internationale', 'Conventions internationales',
    'Pacte international', 'Pactes internationaux', 'Trattato internazionale',
    'Trattati internazionali', 'Trattato di stato', 'Trattati di stato', 'Convenzione internazionale',
    'Convenzioni internazionali', 'Accordo internazionale', 'Accordi internazionali', 'Patto internazionale',
    'Patti internazionali', 'Internationales Vertragsrecht', 'Internationale Vertragsrecht',
    'Internationalen Vertragesrecht', 'Internationalen Vertragsrechts', 'Internationalem Vertragsrecht',
    'Staatsvertrag', 'Staatsverträge', 'Staatsvertrags', 'Staatsvertrages',
    'Ablösungsabkommen', "accord avec l'allemagne", "accordi italo-svizzeri", "Convenzione tra la Svizzera e l'Italia",
    'Doppelbesteuerungsabkommen', 'Doppelbesteuerungsabkommens', 'diritto internazionale convenzionale',
    'droit international conventionnel', 'droit international privé conventionnel'
]
case_completeness_int_treaties['expected_output']['broad'] = [
    'Übereinkommen', 'Abkommen', 'Pakt', 'Pakte', 'Pakts', 'Traité', 'Traités', 'Accord', 'Convention', 'Conventions',
    'Contrat international', 'Contrats internationaux',
    'Pacte', 'Patto', 'Patti', 'pacte entre la Suisse et la France', 'accord pour la double crème',
    'convenzione sulla doppia imposizione',
    'patto di non',

    'staaten abkommen', 'staaten vertragliche', 'staaten vertragspartei', 'staaten übereinkommen',
    'staatliche abkommen', 'staatlichen abkommen', 'staatlichen abkommens', 'staatlichen vertragsrecht',
    'staatlichen verträgen', 'staatlichen Übereinkommen', 'staatlichen Übereinkommens', 'staatlicher abkommen',
    'staatlicher vertrag', 'staatliches abkommen', 'staatsgebiet verträge'
]

# keyword_completeness: for testing if all expected keywords related with international customary law are extracted.
case_completeness_customary_int_law = {'input_item': RulingItem(), 'expected_output': {}}
case_completeness_customary_int_law['input_item']['core_issue'] = '''
    Droit international coutumier
    Droit coutumier international
    Droit coutumier
    Coutumier
    Coutume
    Coutume internationale
    Völkergewohnheitsrecht
    Völkergewohnheitsrechts
    internationales Gewohnheitsrecht
    internationale Gewohnheitsrecht
    internationalen Gewohnheitsrecht
    internationalen Gewohnheitsrechts
    internationalem Gewohnheitsrecht
    völkerrechtliches Gewohnheitsrecht
    völkerrechtliche Gewohnheitsrecht
    völkerrechtlichen Gewohnheitsrechts
    völkerrechtlichem Gewohnheitsrecht
    gewohnheitsrechtlich (too broad)
    gewohnheitsrechtliche
    gewohnheitsrechtlichem
    gewohnheitsrechtlichen
    gewohnheitsrechtlicher
    gewohnheitsrechtliches Völkerrecht
    gewohnheitsrechtliche Völkerrecht
    gewohnheitsrechtlichen Völkerrecht
    gewohnheitsrechtlichen Völkerrechts
    gewohnheitsrechtlichem Völkerrecht
    opinio juris
    opinio iuris
    diritto consuetudinario
    diritto internazionale consuetudinario
    diritto consuetudinario internazionale
    consuetudinario
    consuetudine internazionale
'''
case_completeness_customary_int_law['expected_output']['broad'] = [
    'Droit coutumier', 'Coutumier', 'Coutume', 'Droit coutumier','Coutumier',
    'gewohnheitsrechtlich', 'gewohnheitsrechtliche', 'gewohnheitsrechtlichem', 'gewohnheitsrechtlichen',
    'gewohnheitsrechtlicher', 'diritto consuetudinario', 'consuetudinario'
]
case_completeness_customary_int_law['expected_output']['clear'] = [
    'Droit international coutumier', 'Droit coutumier international', 'Coutume internationale',
    'Völkergewohnheitsrecht', 'Völkergewohnheitsrechts', 'internationales Gewohnheitsrecht',
    'internationale Gewohnheitsrecht', 'internationalen Gewohnheitsrecht', 'internationalen Gewohnheitsrechts',
    'internationalem Gewohnheitsrecht', 'völkerrechtliches Gewohnheitsrecht', 'völkerrechtliche Gewohnheitsrecht',
    'völkerrechtlichen Gewohnheitsrechts', 'völkerrechtlichem Gewohnheitsrecht', 'gewohnheitsrechtliches Völkerrecht',
    'gewohnheitsrechtliche Völkerrecht', 'gewohnheitsrechtlichen Völkerrecht', 'gewohnheitsrechtlichen Völkerrechts',
    'gewohnheitsrechtlichem Völkerrecht', 'opinio juris', 'opinio iuris', 'diritto internazionale consuetudinario',
    'diritto consuetudinario internazionale', 'consuetudine internazionale'
]

# keyword completeness: for testing if all expected keywords related with international law in general are extracted.
case_completeness_int_law_in_general = {'input_item': RulingItem(), 'expected_output': {}}
case_completeness_int_law_in_general['input_item']['core_issue'] = '''
    ius gentium
    droit des gens
    Völkerrecht
    Völkerrechts
    Völkerrechtlich
    Völkerrechtliche
    Völkerrechtlichen
    Völkerrechtliches
    Internationales Recht
    Internationale Recht
    Internationalen Rechts
    Internationalem Recht
    Internationales Privatrecht
    Internationale Privatrecht
    Internationalen Privatrechts
    Internationalem Privatrecht
    Droit international
    Droit international public
    Droit international privé
    Droit privé international
    Droit public international
    Droits internationaux
    Diritto internazionale
    Diritto internazionale pubblico
    Diritto internazionale privato
    Diritti internazionali
    Diritto pubblico internazionale
    Diritto privato internazionale

    # following cases should not be extracted...
    Diritto internazionale convenzionale
    droit international conventionnel
    droit international coutumier
    droit international privé conventionnel
    droit international public coutumier
    internationalen gewohnheitsrechts
    internationalen menschenrechtskonventionen
    internationalen menschenrechtspakte
    internationalen vertragsrechts
    völkerrechtlichen gewohnheitsrecht
    völkerrechtsverträgen
    völkervertragsrechts
'''
case_completeness_int_law_in_general['expected_output']['clear'] = [
    'Völkerrecht', 'Völkerrechts', 'Völkerrechtlich', 'Völkerrechtliche', 'Völkerrechtlichen', 'Völkerrechtliches',
    'Internationales Recht', 'Internationale Recht', 'Internationalen Rechts', 'Internationalem Recht',
    'Internationales Privatrecht', 'Internationale Privatrecht', 'Internationalen Privatrechts',
    'Internationalem Privatrecht', 'Droit international', 'Droit international public', 'Droit international privé',
    'Droit privé international', 'Droit public international', 'Droits internationaux', 'Diritto internazionale',
    'Diritto internazionale pubblico', 'Diritto internazionale privato', 'Diritti internazionali',
    'Diritto pubblico internazionale', 'Diritto privato internazionale'

]
case_completeness_int_law_in_general['expected_output']['broad'] = [
    'ius gentium', 'droit des gens'
]

case_omit_kw_followed_by_number = {'input_item': RulingItem()}
case_omit_kw_followed_by_number['input_item']['core_issue'] = '''
Droit international 1988
Droit international vol
Droit international xxxiv
Diritto internazionale 1981
accordo 13
Internationales Recht XIV
'''



case_metadata_extraction = {'title_of_judgement': [], 'date': []}

case_metadata_extraction['title_of_judgement'] = [
    '88. Auszug aus dem Urteil der Schuldbetreibungs- und Konkurskammer vom 18. November 1998 i.S. F. (Beschwerde)',
    '26\\. Kreisschreiben, Circulaire, Circolare. (11.12.1959)',
    "9. Beschluss der I. öffentlich-rechtlichen Abteilung i. S. Flughafen Zürich AG und Kanton Zürich gegen X. und Eidgenössische Schätzungskommission Kreis 10 (Beschwerde in öffentlich-rechtlichen Angelegenheiten)\nC_100/2011 / 1C_102/2011 vom 9. Dezember 2011",
    "21. Entscheid vom 30. August 1957 i.S. Hächler.",
    "7. Auszug aus dem Urteil der I. sozialrechtlichen Abteilung in Sachen A. gegen Sozialversicherungsgericht des Kantons Zürich (Beschwerde in öffentlich-rechtlichen Angelegenheiten)\n8C_310/2014 vom 31. März 2015",

    "89. Extrait de l'arrêt de la Ire Cour civile du 13 novembre 1998 dans la cause Banque Audi (Suisse) S.A. contre Volkswagen Bank GmbH (recours en réforme)",
    "9. Extrait de l'arrêt de la IIe Cour de droit public en la cause X. SàrL contre Administration fiscale cantonale genevoise (recours en matière de droit public)\n2C_897/2008 du 1er octobre 2009",
    "10. Extrait de l'arrêt de la Ire Cour de droit civil dans les causes X. SA contre Y. et Z. (recours en matière civile)\n4A_489/2011 / 4A_491/2011 du 10 janvier 2012",

    '11. Estratto della sentenza 10 giugno 1988 della Camera delle esecuzioni e dei fallimenti nella causa X. contro Y. e Ufficio esecuzione e fallimenti di Lugano (ricorso)',
    '68. Estratto della sentenza 1o luglio 1955 della Corte di Cassazione penale nella causa X e Y contro Procuratore pubblico sottocenerino.',
    '73. Sentenza della II Corte civile del 11 novembre 1955 nella causa Intervisa SA e Visafin SA contro Visa SA, in liquidazione concordataria.',
    "62\\. Estratto della sentenza della II Corte di diritto sociale nella causa Allianz Suisse Società di Assicurazioni sulla Vita SA contro K. (ricorso in materia di diritto pubblico)\n9C_680/2011 dell'11 maggio 2012",
    "24. Estratto della sentenza 29 gennaio 1963 della I Camera civile nelle cause vertenti fra J. R. Geigy SA Basilea e 1) Istituto De Angeli S.p.A. Milano, 2) Unipharma SA Lugano, 3) Diasan SA Basilea.",

    "12. Extract da la sentenzia da la I. partiziun da dretg public concernent il cas Touring Club Svizra cunter A. e cunparticipads sco er Vischnanca da Sumvitg e Departament da giustia, segirezza e sanadad dal chantun Grischun (recurs da dretg public)\n1C_160/2012 dals 10 da december 2012"
]

case_metadata_extraction['date'] = [datetime.strptime('18.11.1998', '%d.%m.%Y'),
                                    datetime.strptime('11.12.1959', '%d.%m.%Y'),
                                    datetime.strptime('09.12.2011', '%d.%m.%Y'),
                                    datetime.strptime('30.08.1957', '%d.%m.%Y'),
                                    datetime.strptime('31.03.2015', '%d.%m.%Y'),

                                    datetime.strptime('13.11.1998', '%d.%m.%Y'),
                                    datetime.strptime('01.10.2009', '%d.%m.%Y'),
                                    datetime.strptime('10.01.2012', '%d.%m.%Y'),

                                    datetime.strptime('10.06.1988', '%d.%m.%Y'),
                                    datetime.strptime('01.07.1955', '%d.%m.%Y'),
                                    datetime.strptime('11.11.1955', '%d.%m.%Y'),
                                    datetime.strptime('11.05.2012', '%d.%m.%Y'),
                                    datetime.strptime('29.01.1963', '%d.%m.%Y'),

                                    datetime.strptime('10.12.2012', '%d.%m.%Y')]
case_metadata_extraction['parties'] = [
    {'claimant': 'F.'},
    None,
    {'claimant': 'Flughafen Zürich AG und Kanton Zürich',
     'defendant': 'X. und Eidgenössische Schätzungskommission Kreis 10'},
    {'claimant': 'Hächler'},
    {'claimant': 'A.', 'defendant': 'Sozialversicherungsgericht des Kantons Zürich'},

    {'claimant': 'Banque Audi (Suisse) S.A.', 'defendant': 'Volkswagen Bank GmbH'},
    {'claimant': 'X. SàrL', 'defendant': 'Administration fiscale cantonale genevoise'},
    {'claimant': 'X. SA', 'defendant': 'Y. et Z.'},

    {'claimant': 'X.', 'defendant': 'Y. e Ufficio esecuzione e fallimenti di Lugano'},
    {'claimant': 'X e Y', 'defendant': 'Procuratore pubblico sottocenerino'},
    {'claimant': 'Intervisa SA e Visafin SA', 'defendant': 'Visa SA, in liquidazione concordataria'},
    {'claimant': 'Allianz Suisse Società di Assicurazioni sulla Vita SA', 'defendant': 'K.'},
    {'claimant': 'vertenti fra J. R. Geigy SA Basilea e 1) Istituto De Angeli S.p.A. Milano, 2) Unipharma SA Lugano, 3) Diasan SA Basilea'},

    {'claimant': 'Touring Club Svizra',
     'defendant': 'A. e cunparticipads sco er Vischnanca da Sumvitg e Departament da giustia, segirezza e sanadad dal chantun Grischun'}
]
case_metadata_extraction['extracted_department'] = [
    'Schuldbetreibungs- und Konkurskammer',
    None,
    'I. öffentlich-rechtlichen Abteilung',
    None,
    'I. sozialrechtlichen Abteilung',

    'la Ire Cour civile',
    'la IIe Cour de droit public',
    'la Ire Cour de droit civil',

    'Camera delle esecuzioni e dei fallimenti',
    'Corte di Cassazione penale',
    'II Corte civile',
    'II Corte di diritto sociale',
    'I Camera civile',

    'I. partiziun da dretg public'
]
case_metadata_extraction['department_tag'] = [
    'Debt Recovery and Bankruptcy',
    None,
    'Public Law',
    None,
    'Social Insurance Law',

    'Private Law',
    'Public Law',
    'Private Law',

    'Debt Recovery and Bankruptcy',
    'Criminal Law',
    'Private Law',
    'Social Insurance Law',
    'Private Law',

    'Public Law'
]
