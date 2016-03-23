#!/usr/bin/env python
# coding: utf-8
'''
Created on 2016-03-23

@author: alex
'''
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis import queue,scheduler,dupefilter 
from scrapy.core import engine,scheduler as sdr
class BroadSpider(CrawlSpider):
    """
    broad crawl,speed test
    """
    name = 'broadcrawl'
    allowed_domains = ['anjuke.com','sina.com','sohu.com','qq.com','csdn.net','163.com','58.com']
    
    start_urls = ['http://www.sina.com.cn/','http://www.163.com/','http://www.csdn.net/',
                  'http://blog.sohu.com/','http://blog.qq.com/','http://www.qq.com/','http://anjuke.com/','http://sh.58.com/']
    rules = [
             Rule(LinkExtractor(allow=()),callback='parse_item',follow=True),
             ]
    def parse_item(self,response):
        item = {}
        item['url'] = response.url
        item['content'] = response.body
        return item