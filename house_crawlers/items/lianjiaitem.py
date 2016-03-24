#!/usr/bin/env python
# coding: utf-8
'''
Created on 2016-03-24

@author: alex
'''
import scrapy
from scrapy import Item

class LianJiaItem(Item):
    house_name = scrapy.Field()
    house_index_url = scrapy.Field()
    house_price = scrapy.Field()
    house_address = scrapy.Field()
    longtitude_latitude = scrapy.Field()