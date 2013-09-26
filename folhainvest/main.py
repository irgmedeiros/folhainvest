# coding: utf-8
#!/usr/bin/python
from scrapy.xlib.pydispatch import dispatcher

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log, signals
from folhainvest.spiders.Finvest_spider import Finvest_spider


def stop_reactor():
    reactor.stop()

dispatcher.connect(stop_reactor, signal=signals.spider_closed)
spider = Finvest_spider(domain='folhainvest.folha.com.br')
crawler = Crawler(Settings())
crawler.configure()
crawler.crawl(spider)
crawler.start()
log.start(loglevel=log.DEBUG)
log.msg('Running reactor...')
reactor.run()  # the script will block here until the spider is closed
log.msg('Reactor stopped.')


