# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import sqlite3
from os import path

from scrapy import signals, log
from scrapy.contrib.exporter import JsonLinesItemExporter


class FolhainvestPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonExportPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        json_path = os.path.join('dbs', '%s.json' % spider.name)
        file = open(json_path, 'w+b')
        self.files[spider] = file
        self.exporter = JsonLinesItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        log.msg("process_item", level=log.DEBUG)
        return item


class SQLiteStorePipeline(object):
    def __init__(self):
        self.conn = None
        self.filename = 'data.sqlite'
        self.database = os.path.join('dbs', self.filename)

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.initialize, signals.spider_opened)
        crawler.signals.connect(pipeline.finalize, signals.spider_closed)
        return pipeline

    def process_item(self, item, domain):
        try:
            self.conn.execute('insert into folhainvest values(?,?,?)',
                              (item['symbol'], item['name'], unicode(domain)))
        except:
            print 'Failed to insert item: ' + item['name']
        return item

    def initialize(self):
        if path.exists(self.database):
            self.conn = sqlite3.connect(self.database)
        else:
            self.conn = self.create_table()

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def create_table(self):
        conn = sqlite3.connect(self.database)
        conn.execute("""create table folhainvest
                     (symbol text primary key, name text, domain text)""")
        conn.commit()
        return conn