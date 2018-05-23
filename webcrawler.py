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
        print('hi')
        writer = open("valid.txt", 'w')
        writer.write(response.status)
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
