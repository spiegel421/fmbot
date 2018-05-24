import scrapy, sys, os
from os.path import dirname
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from webcrawler.webcrawler.spiders import username_spider, top_ratings_spider
from multiprocessing import Process

s = Settings()
s.setmodule("webcrawler.webcrawler.settings")

def check_valid_username(username):
    def f():
        u_s = username_spider.UsernameSpider()
        process = CrawlerProcess(s)
        process.crawl(u_s, username=username)
        process.start()

    p = Process(target=f)
    p.start()
    p.join()

    with open("webcrawler/webcrawler/temp.txt", 'r') as reader:
        return reader.read()

def get_top_ratings(username, genre):    
    def f():
        t_r_s = top_ratings_spider.TopRatingsSpider()
        process = CrawlerProcess(s)
        process.crawl(t_r_s, username=username, genre=genre)
        process.start()

    p = Process(target=f)
    p.start()
    p.join()

    with open("webcrawler/webcrawler/temp.csv", 'r') as reader:
        return reader.read()

get_top_ratings("appellation1", "metal")
