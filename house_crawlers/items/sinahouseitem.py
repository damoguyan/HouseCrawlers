# coding: utf-8
import scrapy
from scrapy import Item

class SinahouseItem(Item):
    house_name = scrapy.Field()
    house_index_url = scrapy.Field()
    house_price = scrapy.Field()
    house_address = scrapy.Field()
    longtitude_latitude = scrapy.Field()