# contains dummy scrapy item for testing purposes.

from scraping.rulings import RulingItem

case_incomplete = {'input_item': RulingItem(), 'expected_output': RulingItem()}

case_incomplete['input_item']['core_issue'] = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam '\
                                              'nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, '\
                                              'sed diam voluptua. At vero eos et accusam et justo duo dolores et ea '\
                                              'rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem '\
                                              'ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur '\
                                              'sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et '\
                                              'dolore magna aliquyam erat, sed Abkommen. At vero eos et accusam et '\
                                              'justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea '\
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
