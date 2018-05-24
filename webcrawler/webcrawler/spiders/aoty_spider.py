import scrapy, os, sys
from os.path import dirname
from scrapy.crawler import CrawlerProcess

class AotySpider(scrapy.Spider):
    name = 'gettopratings'
    allowed_domains = ['rateyourmusic.com/']

    def __init__(self, username='', year='', webpage='', **kwargs):
        if year == '':
            self.start_urls = ["https://rateyourmusic.com/collection/"+username+"/strm_relyear,ss.rd/2018"+webpage]
        else:
            self.start_urls = ["https://rateyourmusic.com/collection/"+username+"/strm_relyear,ss.rd/"+year+"/"+webpage]
        
        super().__init__(**kwargs)
 
    def parse(self, response):
        body = response.css(".mbgen tr")
        for rating in body[1:]:
            yield {
                'artist': rating.css("a.artist::text").extract_first(),
                'artist_link': rating.css("a.artist::attr(href)").extract_first(),
                'album': rating.css("a.album::text").extract_first(),
                'album_link': rating.css("a.album::attr(href)").extract_first(),
                'rating': rating.css("td.or_q_rating_date_s img::attr(title)").extract_first(),
                }
