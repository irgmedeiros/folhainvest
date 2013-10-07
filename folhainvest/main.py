# coding: utf-8
#!/usr/bin/python

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log, signals
from folhainvest.spiders.Finvest_spider import Finvest_spider
from scrapy.utils.project import inside_project, get_project_settings


def stop_reactor(spider, reason):
    log.msg(spider.name + ' stopped.')
    reactor.stop()


spider = Finvest_spider(domain='folhainvest.folha.com.br')

settings = get_project_settings()
#crawler = Crawler(Settings())
crawler = Crawler(settings)
crawler.signals.connect(stop_reactor, signal=signals.spider_closed)
crawler.configure()
crawler.crawl(spider)
crawler.start()
log.start(loglevel=log.DEBUG)
log.msg('Running reactor...')
reactor.run()  # the script will block here until the spider is closed
log.msg('Reactor stopped.')

l = log.log.discardLogs()
print s


from scrapy import cmdline
cmdline.execute("scrapy crawl finvest_spider".split())


