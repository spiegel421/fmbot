import scrapy, os, sys
from os.path import dirname
from scrapy.crawler import CrawlerProcess

class TopRatingsSpider(scrapy.Spider):
    name = 'gettopratings'
    allowed_domains = ['rateyourmusic.com/']

    def __init__(self, username='', genre='', webpage='', **kwargs):
        if genre == '':
            self.start_urls = ["https://rateyourmusic.com/collection/"+username+"/recent,ss.rd/"+webpage]
        else:
            self.start_urls = ["https://rateyourmusic.com/collection/"+username+"/strm_h,ss.rd/"+genre+"/"+webpage]
        
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
