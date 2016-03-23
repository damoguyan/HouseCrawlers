#!/usr/bin/env python
# coding: utf-8
'''
Created on 2016-03-22

@author: alex
'''
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class AnjukeSpider(CrawlSpider):
    """
    安居客楼盘爬虫
    """
    name = 'anjuke'
    allowed_domains = ['anjuke.com',]
    start_urls = ['http://www.anjuke.com/sy-city.html',]
    rules = [
             #各城市链接跟进
             Rule(LinkExtractor(allow=('^http://\w+.anjuke.com$')),follow=True),
             #城市新楼盘页面跟进
             Rule(LinkExtractor(allow=('^http://\w+.fang.anjuke.com$')),follow=True),
             #城市新楼盘翻页跟进
             Rule(LinkExtractor(allow=('^http://\w+.fang.anjuke.com/\w+/s\?p=\d+$')),follow=True),
             
             ]