import scrapy
from scrapy.exporters import CsvItemExporter

class CsvPipeline(object):
    def __init__(self):
        self.file = open("temp.csv", 'wb')
        self.exporter = CsvItemExporter(self.file, unicode)
        self.exporter.start_exporting()
 
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
 
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
