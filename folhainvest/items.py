# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class PortifolioItem(Item):
    name = Field()
    symbol = Field()
    quantity = Field()
    mean = Field()
    current = Field()
    total = Field()
    gainloss = Field()
    percent = Field()


class CotacaoItem(Item):
    name = Field()
    symbol = Field()
    current = Field()
    last_neg = Field()
    oscillation = Field()
    openning = Field()
    close = Field()
    maximum = Field()
    minimun = Field()
    volume = Field()

