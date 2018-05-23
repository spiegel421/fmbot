import scrapy, sys, os
from os.path import dirname
from scrapy import settings
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process

settings_file_path = 'webcrawler.webcrawler.settings' # The path seen from root, ie. from main.py
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)

class UsernameSpider(scrapy.Spider):
    name = 'checkvalidusername'
    handle_httpstatus_list = [404] 
    allowed_domains = ['rateyourmusic.com/']

    def __init__(self, username='', **kwargs):
        self.start_urls = ["https://rateyourmusic.com/~"+username]
        super().__init__(**kwargs)
 
    def parse(self, response):
        writer = open("temp.txt", 'w')
        writer.write(str(response.status))
        writer.close()


def check_valid_username(username):
    def f():
        u_s = UsernameSpider()
        process = CrawlerProcess(get_project_settings())
        process.crawl(u_s, username=username)
        process.start()

    p = Process(target=f)
    p.start()
    p.join()

    with open("temp.txt", 'r') as reader:
        return reader.read()

class TopRatingsSpider(scrapy.Spider):
    name = 'gettopratings'
    allowed_domains = ['rateyourmusic.com/']

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
        t_r_s = TopRatingsSpider()
        process = CrawlerProcess(get_project_settings())
        process.crawl(t_r_s, username=username)
        process.start()

    p = Process(target=f)
    p.start()
    p.join()

    with open("temp.csv", 'r') as reader:
        return reader.read()

check_valid_username("appellation1")
