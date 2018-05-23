import scrapy, sys, os
from os.path import dirname
from scrapy import settings
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import username_spider, top_ratings_spider
from multiprocessing import Process

def check_valid_username(username):
    def f():
        u_s = username_spider.UsernameSpider()
        process = CrawlerProcess(get_project_settings())
        process.crawl(u_s, username=username)
        process.start()

    p = Process(target=f)
    p.start()
    p.join()

    with open("temp.txt", 'r') as reader:
        return reader.read()

def get_top_ratings(username, genre):    
    def f():
        t_r_s = top_ratings_spider.TopRatingsSpider()
        process = CrawlerProcess(get_project_settings())
        process.crawl(t_r_s, username=username)
        process.start()

    p = Process(target=f)
    p.start()
    p.join()

    with open("temp.csv", 'r') as reader:
        return reader.read()

check_valid_username("appellation1")
