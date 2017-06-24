# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Vinyl(scrapy.Item):
    vinyl_sku = scrapy.Field()
    vinyl_upc = scrapy.Field()
    vinyl_url = scrapy.Field()
    vinyl_name = scrapy.Field()
    vinyl_alpha = scrapy.Field()
    vinyl_genre = scrapy.Field()
    vinyl_price = scrapy.Field()
    # vinyl_stock = scrapy.Field()
    vinyl_artist_name = scrapy.Field()
    vinyl_description = scrapy.Field()
