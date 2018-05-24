import scrapy

class UsernameSpider(scrapy.Spider):
    name = 'checkvalidusername'
    handle_httpstatus_list = [404, 302, 303] 
    allowed_domains = ['rateyourmusic.com/']

    def __init__(self, username='', **kwargs):
        self.start_urls = ["https://rateyourmusic.com/~"+username]
        super().__init__(**kwargs)
 
    def parse(self, response):
        writer = open("webcrawler/webcrawler/temp.txt", 'w')
        writer.write(str(response.status))
        writer.close()
