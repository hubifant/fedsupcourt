import scrapy
from scrapy.loader import ItemLoader
from ..items import RulingItem


class RulingSpider(scrapy.Spider):
    name = 'rulings'
    start_urls = ["http://relevancy.bger.ch/cgi-bin/IndexCGI?lang=de"]
    scraped_links = []
    allowed_domains =["relevancy.bger.ch"]

    def parse(self, response):

        volume_links = response.xpath("//tr/td/a[text()[contains(., 'I')]]/@href").extract()
        for link in volume_links:
            url = 'http://relevancy.bger.ch/' + link
            if url not in self.scraped_links and len(self.scraped_links) < 2:
                self.scraped_links.append(url)
                yield scrapy.Request(url, self.parse_year)

    def parse_year(self, response):
        # get ruling links and corresponding ruling ids; process them (create new request)
        rulings = response.xpath('//li/a/@href | //li/a[@href]/text()').extract()
        for link, ruling_id in zip(*[iter(rulings)]*2):
            url = 'http://relevancy.bger.ch/' + link

            if url not in self.scraped_links and len(self.scraped_links) < 10:
                self.scraped_links.append(url)
                request = scrapy.Request(url, self.parse_ruling)
                request.meta['ruling_id'] = ruling_id
                yield request

    def parse_ruling(self, response):

        l = ItemLoader(item=RulingItem(), response=response)
        # the date can be extracted from one of the first two 'paraatf' divs.
        l.add_xpath('date', '(//div[@class="paraatf"])[position()=1 or position()=2]/text()')

        # rubrum is the text before 'regeste' paragraph.
        l.add_xpath('rubrum', '//div[@class="content"]/div[@id="regeste"]/preceding-sibling::div[@class="paraatf"]')
        l.add_xpath('involved_parties', '(//div[@class="paraatf"])[1]/text()')
        l.add_xpath('language', '(//div[@class="paraatf"])[1]/text()')

        # regeste is contained in children of //div[@id="regeste"]
        l.add_xpath('regeste', '//div[@id="regeste"]/child::*')
        l.add_value('ruling_id', response.meta['ruling_id'])
        l.add_value('url', response.url)

        # statement_of_affairs
        l.add_xpath('statement_of_affairs',
                    '//div[span[@id="sachverhalt"]]'                        # navigate to 'sachverhalt'
                    '/following-sibling::div'                               # all following siblings
                    '[following-sibling::div[span[@id="erwaegungen"]]]'     # they must be followed by 'erwägung'
                    '/node()[not(@class="center pagebreak")'                # exclude pagebreak-<div>s
                    '        and not(contains(@name, "page"))]')            # exclude pagebreaks-<a>s

        # references
        l.add_xpath('bge_refs', '//div[@id="highlight_references"]//p[text()[contains(.,"BGE:")]]//a/text()')
        l.add_xpath('art_refs', '//div[@id="highlight_references"]//p[text()[contains(.,"Artikel:")]]//text()')
        yield l.load_item()


