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

            if url not in self.scraped_links and len(self.scraped_links) < 4:
                self.scraped_links.append(url)
                request = scrapy.Request(url, self.parse_ruling)
                request.meta['ruling_id'] = ruling_id
                yield request

    def parse_ruling(self, response):
        bge_nb, volume, ruling_nb = response.meta['ruling_id'].split(' ')
        ruling_id_dict = {
            'bge_nb': int(bge_nb),
            'volume': volume,
            'ruling_nb': int(ruling_nb)
        }
        l = ItemLoader(item=RulingItem(), response=response)
        # l.add_xpath('year', '//tr/td[@valign="top"]/text()')
        l.add_xpath('regeste', '//div[@id="regeste"]//text()')
        # l.add_value('bge_nb', int(bge_nb))
        # l.add_value('volume', volume)
        # l.add_value('ruling_nb', int(ruling_nb))
        l.add_value('ruling_id', ruling_id_dict)
        yield l.load_item()


