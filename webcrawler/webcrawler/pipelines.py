# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter

class CsvPipeline(object):
    def __init__(self):
        self.file = open("webcrawler/webcrawler/temp.csv", 'wb')

    def open_spider(self, spider):
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()
 
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def export_item(self, item):
        self.file.write(item+"\n")
