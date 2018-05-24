# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter

class TopRatingsPipeline(object):
    def __init__(self):
        self.file_name = "webcrawler/webcrawler/temp.csv"
        self.file_handle = None

    def open_spider(self, spider):
        file = open(self.file_name, 'wb')
        self.file_handle = file

    def close_spider(self, spider):
        self.file_handle.close()

    def process_item(self, item, spider):
        self.file.write(item)
        return item
