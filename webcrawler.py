# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor
from multiprocessing import Process

class UsernameSpider(scrapy.Spider):
    name = 'checkvalidusername'
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
        writer = open("valid.txt", 'w')
        if response.status == 404:
            writer.write("False")
        else:
            writer.write("True")
        writer.close()

def check_valid_username(username):
    def f():
        username_spider = UsernameSpider()
        runner = CrawlerRunner()
        d = runner.crawl(username_spider, username=username)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
        
    p = Process(target=f)
    p.start()
    p.join()
    print('success!')

