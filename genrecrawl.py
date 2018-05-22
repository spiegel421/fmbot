# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor


class GenrecrawlSpider(scrapy.Spider):
    name = 'genrecrawl'
    allowed_domains = ['rateyourmusic.com/']
    custom_settings = {
        'DOWNLOAD_DELAY': 10,
        'CONCURRENT_REQUESTS': 1,
        'ROBOTSTXT_OBEY': False,
        'REDIRECT_ENABLED': True,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }

    def __init__(self, artist='', album='', **kwargs):
        self.start_urls = ['https://rateyourmusic.com/release/album/'+artist+'/'+album+'/']
        super().__init__(**kwargs)
 
    def parse(self, response):
        writer = open("genres.txt", 'w')
        genre_table = response.css("tr.release_genres")
        pri_genre_table = genre_table.css("span.release_pri_genres a.genre::text").extract()
        sec_genre_table = genre_table.css("span.release_sec_genres a.genre::text").extract()
        for genre in pri_genre_table:
            writer.write(genre+"\t")
        writer.write("\n")
        for genre in sec_genre_table:
            writer.write(genre+"\t")
        writer.close()

def edit_genre_file(artist, album):
    genre_spider = GenrecrawlSpider()
    runner = CrawlerRunner()
    d = runner.crawl(genre_spider, artist=artist, album=album)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
    reactor.stop()
