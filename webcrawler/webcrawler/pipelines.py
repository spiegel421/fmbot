# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter

class TopRatingsPipeline(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_handle = None

    @classmethod
    def from_crawler(cls, crawler):
        output_file_name = "webcrawler/webcrawler/temp.csv"
        return cls(output_file_name)

    def open_spider(self, spider):
        file = open(self.file_name, 'wb')
        self.file_handle = file

        self.exporter = CsvItemExporter(file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        print('Custom Exporter closed')

        self.exporter.finish_exporting()
        self.file_handle.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        self.file.write(item)
        return item
