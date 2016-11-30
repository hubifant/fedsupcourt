# contains dummy scrapy item for testing purposes.

from scraping.rulings import RulingItem

# case_incomplete: for testing a simple keyword extraction in the case where a ruling does not contain all 3 chapters
case_incomplete = {'input_item': RulingItem(), 'expected_output': RulingItem()}
case_incomplete['input_item']['core_issue'] = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam ' \
                                              'nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, ' \
                                              'sed diam voluptua. At vero eos et accusam et justo duo dolores et ea ' \
                                              'rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ' \
                                              'ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur ' \
                                              'sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et ' \
                                              'dolore magna aliquyam erat, sed Abkommen. At vero eos et accusam et ' \
                                              'justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea ' \
                                              'takimata sanctus est Lorem ipsum dolor sit amet.'
case_incomplete['input_item']['paragraph'] = 'The chapter \'paragraph\' does not contain any keyword.'

case_incomplete['expected_output']['international_treaties'] = {
    'contexts': [{
        'chapter': 'core_issue',
        'keyword': 'sed Abkommen',
        'sentence': 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt '
                    'ut labore et dolore magna aliquyam erat, sed Abkommen.'
    }],
    'keywords': {'sed Abkommen': 1}
}

# case_keyword_completeness: for testing if all expected keywords related with international treaties are extracted.
case_completeness_int_treaties = {'input_item': RulingItem(), 'expected_output': RulingItem()}
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
    Übereinkommen (potentially too broad?)
    Abkommen (potentially too broad?)
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
    Pakt (too broad?)
    Pakte (idem)
    Pakts (idem)
    Traité international
    Traités internationaux
    Traité
    Traités
    Accord international
    Accords internationaux
    Accord (probably too broad)
    Convention internationale
    Conventions internationales
    Convention (too broad)
    Conventions (idem)
    Contrat international
    Contrats internationaux
    Pacte international
    Pactes internationaux
    Pacte (too broad?)
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
    Patto (probably too broad)
    Patti
Update 25.11.16:
    Internationales Vertragsrecht
    Internationale Vertragsrecht
    Internationalen Vertragesrecht
    Internationalen Vertragsrechts
    Internationalem Vertragsrecht
Updatevorschläge Nicolas
    Staatsvertrag
    Staatsverträge
    Staatsvertrags
    Staatsvertrages
    Doppelbesteuerungsabkommen (Bsp für einen bestimmten Vertrag)
    Doppelbesteuerungsabkommens
    convenzione sulla doppia imposizione
    patto di non aggressione
'''
case_completeness_int_treaties['expected_output'] = [
    'Völkerrechtliches Abkommen', 'Völkerrechtliche Abkommen', 'Völkerrechtlichen Abkommen',
    'Völkerrechtlichen Abkommens', 'Völkerrechtlicher Abkommen', 'Internationales Abkommen', 'Internationale Abkommen',
    'Internationalen Abkommen', 'Internationalen Abkommens', 'Internationaler Abkommen',
    'Völkerrechtliches Übereinkommen', 'Völkerrechtliche Übereinkommen', 'Völkerrechtlichen Übereinkommen',
    'Völkerrechtlichen Übereinkommens', 'Völkerrechtlicher Übereinkommen', 'Internationales Übereinkommen',
    'Internationale Übereinkommen', 'Internationalen Übereinkommen', 'Internationalen Übereinkommens',
    'Internationaler Übereinkommen', 'Übereinkommen', 'Abkommen',
    'Völkerrechtlicher Vertrag', 'Völkerrechtlichen Vertrags', 'Völkerrechtlichen Vertrages',
    'Völkerrechtlichen Vertrag', 'Völkerrechtliche Verträge', 'Völkerrechtlichen Verträge',
    'Völkerrechtlicher Verträge', 'Internationaler Vertrag', 'Internationalen Vertrags', 'Internationalen Vertrages',
    'Internationalen Vertrag', 'Internationale Verträge', 'Internationalen Verträge', 'Internationaler Verträge',
    'Internationaler Pakt', 'Internationalen Pakts', 'Internationalen Paktes', 'Internationalen Pakt',
    'Internationale Pakte', 'Internationalen Pakte', 'Internationaler Pakte', 'Völkerrechtlicher Pakt',
    'Völkerrechtlichen Pakts', 'Völkerrechtlichen Paktes', 'Völkerrechtlichen Pakt', 'Völkerrechtliche Pakte',
    'Völkerrechtlichen Pakte', 'Völkerrechtlicher Pakte', 'Pakt', 'Pakte', 'Pakts',
    'Traité international', 'Traités internationaux', 'Traité', 'Traités', 'Accord international',
    'Accords internationaux', 'Accord', 'Convention internationale', 'Conventions internationales',
    'Convention', 'Conventions', 'Contrat international', 'Contrats internationaux',
    'Pacte international', 'Pactes internationaux', 'Pacte', 'Trattato internazionale',
    'Trattati internazionali', 'Trattato di stato', 'Trattati di stato', 'Convenzione internazionale',
    'Convenzioni internazionali', 'Accordo internazionale', 'Accordi internazionali', 'Patto internazionale',
    'Patti internazionali', 'Patto', 'Patti', 'Internationales Vertragsrecht', 'Internationale Vertragsrecht',
    'Internationalen Vertragesrecht', 'Internationalen Vertragsrechts', 'Internationalem Vertragsrecht',
    'Staatsvertrag', 'Staatsverträge', 'Staatsvertrags', 'Staatsvertrages', 'Doppelbesteuerungsabkommen',
    'Doppelbesteuerungsabkommens', 'convenzione sulla doppia', 'patto di non'
]

# keyword_completeness: for testing if all expected keywords related with international customary law are extracted.
case_completeness_customary_int_law = {'input_item': RulingItem(), 'expected_output': RulingItem()}
case_completeness_customary_int_law['input_item']['core_issue'] = '''
    Droit international coutumier
    Droit coutumier international
    Coutumier (too broad)
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
    gewohnheitsrechtliches Völkerrecht
    gewohnheitsrechtliche Völkerrecht
    gewohnheitsrechtlichen Völkerrecht
    gewohnheitsrechtlichen Völkerrechts
    gewohnheitsrechtlichem Völkerrecht
    gewohnheitsrechtlich (too broad)
    ius gentium
    droit des gens (too broad, I think, judging from a past research project)
    opinio juris
    opinio iuris
    diritto consuetudinario
    diritto internazionale consuetudinario
    diritto consuetudinario internazionale
    consuetudinario (too broad)
    consuetudine internazionale
'''
case_completeness_customary_int_law['expected_output'] = [
    'Droit international coutumier', 'Droit coutumier international', 'Coutumier', 'Coutume internationale',
    'Völkergewohnheitsrecht', 'Völkergewohnheitsrechts', 'internationales Gewohnheitsrecht',
    'internationale Gewohnheitsrecht', 'internationalen Gewohnheitsrecht', 'internationalen Gewohnheitsrechts',
    'internationalem Gewohnheitsrecht', 'völkerrechtliches Gewohnheitsrecht', 'völkerrechtliche Gewohnheitsrecht',
    'völkerrechtlichen Gewohnheitsrechts', 'völkerrechtlichem Gewohnheitsrecht', 'gewohnheitsrechtliches Völkerrecht',
    'gewohnheitsrechtliche Völkerrecht', 'gewohnheitsrechtlichen Völkerrecht', 'gewohnheitsrechtlichen Völkerrechts',
    'gewohnheitsrechtlichem Völkerrecht', 'gewohnheitsrechtlich', 'ius gentium', 'droit des gens', 'opinio juris',
    'opinio iuris', 'diritto consuetudinario', 'diritto internazionale consuetudinario',
    'diritto consuetudinario internazionale', 'consuetudinario', 'consuetudine internazionale'
]

# keyword completeness: for testing if all expected keywords related with international law in general are extracted.
case_completeness_int_law_in_general = {'input_item': RulingItem(), 'expected_output': RulingItem()}
case_completeness_int_law_in_general['input_item']['core_issue'] = '''
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
    Droit international
    Droit international public
    Droit international privé
    Droits internationaux
    Diritto internazionale
    Diritto internazionale pubblico
    Diritto internazionale private
    Diritti internazionali
'''
case_completeness_int_law_in_general['expected_output'] = [
    'Völkerrecht', 'Völkerrechts', 'Völkerrechtlich', 'Völkerrechtliche', 'Völkerrechtlichen', 'Völkerrechtliches',
    'Internationales Recht', 'Internationale Recht', 'Internationalen Rechts', 'Internationalem Recht',
    'Droit international', 'Droit international public', 'Droit international privé', 'Droits internationaux',
    'Diritto internazionale', 'Diritto internazionale pubblico', 'Diritto internazionale private',
    'Diritti internazionali'
]


case_metadata_extraction = {'title_of_judgement': [], 'date': []}

case_metadata_extraction['title_of_judgement'] = [
    '88. Auszug aus dem Urteil der Schuldbetreibungs- und Konkurskammer vom 18. November 1998 i.S. F. (Beschwerde)',
    '26\\. Kreisschreiben, Circulaire, Circolare. (11.12.1959)',
    "9. Beschluss der I. öffentlich-rechtlichen Abteilung i. S. Flughafen Zürich AG und Kanton Zürich gegen X. und Eidgenössische Schätzungskommission Kreis 10 (Beschwerde in öffentlich-rechtlichen Angelegenheiten)\nC_100/2011 / 1C_102/2011 vom 9. Dezember 2011",
    "21. Entscheid vom 30. August 1957 i.S. Hächler.",
    "7. Auszug aus dem Urteil der I. sozialrechtlichen Abteilung i.S A. gegen Sozialversicherungsgericht des Kantons Zürich (Beschwerde in öffentlich-rechtlichen Angelegenheiten)\n8C_310/2014 vom 31. März 2015",

    "89. Extrait de l'arrêt de la Ire Cour civile du 13 novembre 1998 dans la cause Banque Audi (Suisse) S.A. contre Volkswagen Bank GmbH (recours en réforme)",
    "9. Extrait de l'arrêt de la IIe Cour de droit public en la cause X. SàrL contre Administration fiscale cantonale genevoise (recours en matière de droit public)\n2C_897/2008 du 1er octobre 2009",
    "10. Extrait de l'arrêt de la Ire Cour de droit civil dans les causes X. SA contre Y. et Z. (recours en matière civile)\n4A_489/2011 / 4A_491/2011 du 10 janvier 2012",

    '11. Estratto della sentenza 10 giugno 1988 della Camera delle esecuzioni e dei fallimenti nella causa X. contro Y. e Ufficio esecuzione e fallimenti di Lugano (ricorso)',
    '68. Estratto della sentenza 1o luglio 1955 della Corte di Cassazione penale nella causa X e Y contro Procuratore pubblico sottocenerino.',
    '73. Sentenza 11 novembre 1955 della II Corte civile nella causa Intervisa SA e Visafin SA contro Visa SA, in liquidazione concordataria.',
    "62\\. Estratto della sentenza della II Corte di diritto sociale nella causa Allianz Suisse Società di Assicurazioni sulla Vita SA contro K. (ricorso in materia di diritto pubblico)\n9C_680/2011 dell'11 maggio 2012",

    "12. Extract da la sentenzia da la I. partiziun da dretg public concernent il cas Touring Club Svizra cunter A. e cunparticipads sco er Vischnanca da Sumvitg e Departament da giustia, segirezza e sanadad dal chantun Grischun (recurs da dretg public)\n1C_160/2012 dals 10 da december 2012"
]

case_metadata_extraction['date'] = ['18.11.1998',
                                    '11.12.1959',
                                    '09.12.2011',
                                    '30.08.1957',
                                    '31.03.2015',

                                    '13.11.1998',
                                    '01.10.2009',
                                    '10.01.2012',

                                    '10.06.1988',
                                    '01.07.1955',
                                    '11.11.1955',
                                    '11.05.2012',

                                    '10.12.2012']
case_metadata_extraction['parties'] = [
    {'claimant': 'F.'},
    None,
    {'claimant': 'Flughafen Zürich AG und Kanton Zürich',
     'defendant': 'X. und Eidgenössische Schätzungskommission Kreis 10'},
    {'claimant': 'Hächler'},
    {'claimant': 'A.', 'defendant': 'Sozialversicherungsgericht des Kantons Zürich'},

    {'claimant': 'Banque Audi (Suisse) S.A.', 'defendant': 'Volkswagen Bank GmbH'},
    {'claimant': 'X. SàrL', 'defendant': 'Administration fiscale cantonale genevoise'},
    {'claimant': 'X. SA' , 'defendant': 'Y. et Z.'},

    {'claimant': 'X.', 'defendant': 'Y. e Ufficio esecuzione e fallimenti di Lugano'},
    {'claimant': 'X e Y', 'defendant': 'Procuratore pubblico sottocenerino'},
    {'claimant': 'Intervisa SA e Visafin SA', 'defendant': 'Visa SA, in liquidazione concordataria'},
    {'claimant': 'Allianz Suisse Società di Assicurazioni sulla Vita SA', 'defendant': 'K.'},

    {'claimant': 'Touring Club Svizra',
     'defendant': 'A. e cunparticipads sco er Vischnanca da Sumvitg e Departament da giustia, segirezza e sanadad dal chantun Grischun'}
]