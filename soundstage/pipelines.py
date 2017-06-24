# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class SoundstagePipeline(object):

    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):

        # drop empty prices from price list
        item['vinyl_price'].remove("")

        # dump results to json file
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
