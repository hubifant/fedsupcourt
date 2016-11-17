from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scraping.rulings import RulingSpider


def scrape_rulings():
    # set the format of the logging messages
    configure_logging({'LOG_FORMAT': '%(levelname)s | %(message)s'})
    runner = CrawlerRunner()

    # start the crawler
    d = runner.crawl(RulingSpider)

    # add callback that stops the reactor after RulingSpider has finished running
    d.addBoth(lambda _: reactor.stop())

    # the script will be blocked at the following line until the crawling is finished
    reactor.run()


scrape_rulings()
