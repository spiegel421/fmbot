import scrapy, os, sys
from os.path import dirname
from scrapy.crawler import CrawlerProcess

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
