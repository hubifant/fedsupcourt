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

# case_keyword_completeness: for testing if all expected keywords related with international law are extracted.
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

# case_keyword_completeness: for testing if all expected keywords related with international law are extracted.
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
