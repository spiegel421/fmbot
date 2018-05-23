import scrapy, sys
from os.path import dirname
from scrapy import settings
from scrapy.crawler import CrawlerProcess
from spiders import username, top_ratings
from multiprocessing import Process

sys.path.append(dirname("/Users/justin/Documents/lastfm/webcrawler/"))
s = settings.Settings()
s.setmodule('webcrawler.settings')

def check_valid_username(username):
    def f():
        username_spider = username.UsernameSpider()
        process = CrawlerProcess()
        process.crawl(username_spider, username=username)
        process.start()

    p = Process(target=f)
    p.start()
    p.join()

    with open("temp.txt", 'r') as reader:
        return reader.read()

def get_top_ratings(username, genre):    
    def f():
        top_ratings_spider = top_ratings.TopRatingsSpider()
        process = CrawlerProcess(s)
        process.crawl(top_ratings_spider, username=username)
        process.start()

    p = Process(target=f)
    p.start()
    p.join()

    with open("temp.csv", 'r') as reader:
        return reader.read()
