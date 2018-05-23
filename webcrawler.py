# -*- coding: utf-8 -*-
import scrapy
from scrapy.exporters import CsvItemExporter
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor
from multiprocessing import Process

class CsvPipeline(object):
    def __init__(self):
        self.file = open("temp.csv", 'wb')
        self.exporter = CsvItemExporter(self.file, unicode)
        self.exporter.start_exporting()
 
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
 
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class UsernameSpider(scrapy.Spider):
    name = 'checkvalidusername'
    handle_httpstatus_list = [404] 
    allowed_domains = ['rateyourmusic.com/']
    custom_settings = {
        'DOWNLOAD_DELAY': 10,
        'CONCURRENT_REQUESTS': 1,
        'ROBOTSTXT_OBEY': False,
        'REDIRECT_ENABLED': True,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }

    def __init__(self, username='', **kwargs):
        self.start_urls = ["https://rateyourmusic.com/~"+username]
        super().__init__(**kwargs)
 
    def parse(self, response):
        writer = open("temp.txt", 'w')
        writer.write(str(response.status))
        writer.close()

def check_valid_username(username):
    def f():
        username_spider = UsernameSpider()
        process = CrawlerProcess()
        process.crawl(username_spider, username=username)
        process.start()

    p = Process(target=f)
    p.start()
    p.join()

    with open("temp.txt", 'r') as reader:
        return reader.read()

class TopRatingsSpider(scrapy.Spider):
    name = 'gettopratings'
    allowed_domains = ['rateyourmusic.com/']
    custom_settings = {
        'DOWNLOAD_DELAY': 10,
        'CONCURRENT_REQUESTS': 1,
        'ROBOTSTXT_OBEY': False,
        'REDIRECT_ENABLED': True,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'LOG_STDOUT': True,
        'LOG_FILE': 'temp.txt',
        'ITEM_PIPELINES': {
            'CsvPipeline': 500,
            }
        }

    def __init__(self, username='', genre='', **kwargs):
        self.start_urls = ["https://rateyourmusic.com/collection/"+username+"/strm_h,ss.rd/"+genre]
        super().__init__(**kwargs)
 
    def parse(self, response):
        body = response.css("table.mgen tbody")
        for rating in body.css("tr")[1:]:
            yield {
                'artist': rating.css("a.artist::text").extract_first(),
                'album': rating.css("a.album::text").extract_first(),
                'rating': rating.css("td.or_q_rating_date_s img::attr(title)").extract_first(),
                }

def get_top_ratings(username, genre):
    def f():
        username_spider = UsernameSpider()
        process = CrawlerProcess()
        process.crawl(username_spider, username=username)
        process.start()

    p = Process(target=f)
    p.start()
    p.join()

    with open("temp.csv", 'r') as reader:
        return reader.read()
