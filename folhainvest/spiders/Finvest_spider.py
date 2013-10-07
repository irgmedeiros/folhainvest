# coding: utf-8
import hashlib
from scrapy import log
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import FormRequest, Request
from scrapy.selector import HtmlXPathSelector
from scrapy.conf import settings
from folhainvest.items import PortifolioItem, CotacaoItem
from time import sleep, time


class Finvest_spider(CrawlSpider):
    name = "finvest_spider"
    allowed_domains = [".folhainvest.com.br", "folhainvest.folha.com.br", "login.folha.com.br", ".folha.com.br"]
    login_page = \
        "http://login.folha.com.br/login?done=http%3A%2F%2Ffolhainvest.folha.com.br%2Fcarteira&service=folhainvest"
    start_urls = [
        #"http://login.folha.com.br/login?done=http%3A%2F%2Ffolhainvest.folha.com.br%2Fcarteira&service=folhainvest",
        #"http://folhainvest.folha.com.br/",
        "http://folhainvest.folha.com.br/carteira",
    ]
    extra_domain_names = ["folhainvest", "folha"]

    rules = (
        Rule(SgmlLinkExtractor(allow=r'.+/carteira$'), 'parse_portifolio', follow=True),
        Rule(SgmlLinkExtractor(allow=r'.+/cotacoes$'), 'parse_cotacoes', follow=True),
    )

    #Methods
    def start_requests(self):
        """This function is called before crawling starts."""
        yield Request(url=self.login_page, callback=self.login, dont_filter=True)

    def login(self, response):
        """Generate a login request."""
        # from scrapy.shell import inspect_response
        # inspect_response(response)
        hxs = HtmlXPathSelector(response)

        email = settings.get('FOLHA_USER')
        password = settings.get('FOLHA_PASS')

        challenge = hxs.select("//form[@name='login']/input[@name='challenge']/@value").extract()[0]
        password_challenge = hashlib.md5(challenge + hashlib.md5(password).hexdigest()).hexdigest()

        data = {'email': email,
                'password_challenge': password_challenge,
                'password': password,
                'challenge': challenge,
                r'auth.x': '1',
                r'auth.y': '1',
                'auth': 'Autenticar'
        }

        return [FormRequest.from_response(response,
                                          formname='login',
                                          formdata=data,
                                          callback=self.check_login_response)]

    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """

        if "Log Out" in response.body:
            self.log("\n\nSuccessfully logged in. Let's start crawling!\n\n")
            # Now the crawling can begin..
            yield Request(url='http://folhainvest.folha.com.br/carteira', callback=self.parse_portifolio,
                          dont_filter=True)
        else:
            self.log("\nLogin failed\n", level=log.ERROR)
            # Something went wrong, we couldn't log in, so nothing happens.

    def parse_portifolio(self, response):
        """Extract portifolio data."""

        portifolio = []
        hxs = HtmlXPathSelector(response)

        stock_stats = hxs.select("//table[@class='fiTable']/tr/*/a/parent::*/parent::*")
        for stock_stat in stock_stats:
            pitem = PortifolioItem()
            pitem['name'] = extractor(stock_stat, "td[2]/text()")
            pitem['symbol'] = extractor(stock_stat, "td/a/text()")
            pitem['quantity'] = extractor(stock_stat, "td[5]/text()")
            pitem['mean'] = extractor(stock_stat, "td[6]/text()")
            pitem['current'] = extractor(stock_stat, "td[7]/text()")
            pitem['total'] = extractor(stock_stat, "td[8]/text()")
            pitem['gainloss'] = extractor(stock_stat, "td[9]/text()")
            pitem['percent'] = extractor(stock_stat, "td[10]/text()")

            portifolio.append(pitem)
            yield pitem

        sleep(1)
        yield Request(url='http://folhainvest.folha.com.br')

    def parse_cotacoes(self, response):
        """Extract cotacoes data."""
        # from scrapy.shell import inspect_response
        # inspect_response(response)

        cotacoes = []
        hxs = HtmlXPathSelector(response)

        tabela_cotacoes = hxs.select("//table[@class='fiTable']/tr[position()>1]")
        for cotacao in tabela_cotacoes:
            citem = CotacaoItem()
            citem['name'] = extractor(cotacao, "td[4]/text()")
            citem['symbol'] = extractor(cotacao, "td/a/b/text()")
            citem['current'] = extractor(cotacao, "td[6]/text()")
            citem['last_neg'] = extractor(cotacao, "td[7]/text()")
            citem['oscillation'] = extractor(cotacao, "td[8]/text()")
            citem['openning'] = extractor(cotacao, "td[9]/text()")
            citem['close'] = extractor(cotacao, "td[10]/text()")
            citem['maximum'] = extractor(cotacao, "td[11]/text()")
            citem['minimun'] = extractor(cotacao, "td[12]/text()")
            citem['volume'] = extractor(cotacao, "td[13]/text()")

            cotacoes.append(citem)
            yield citem

        sleep(1)
        # yield Request(url='http://folhainvest.folha.com.br/carteira', callback=self.parse_portifolio, dont_filter=True)


def extractor(xpathselector, selector):
    """
    Helper function that extract info from xpathselector object
    using the selector constrains.
    """
    val = xpathselector.select(selector).extract()
    return val[0] if val else None


SPIDER = Finvest_spider()
