#!/usr/bin/env python
# coding: utf-8
'''
Created on 2016-03-21

@author: alex
'''

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from items.sinahouseitem import SinahouseItem

class SinahouseSpider(CrawlSpider):
    """
    新浪乐居楼盘爬虫
    """
    name = 'sinahouse'
    allowed_domains = ['house.sina.com',]
    start_urls = ['http://data.house.sina.com.cn/sh/search/?bcity=sh&keyword=',]
    costom_settings = {}
    rules = [
             #具体楼盘链接提取
             Rule(LinkExtractor(allow=("http://data.house.sina.com.cn/\w+\d+\?\w+=\w+bt\d*")), callback='parse_item'),
             #当前城市下,楼盘下一页链接跟进
             Rule(LinkExtractor(allow=("/\w+/search-\d+.*")), follow=True),
             #其他城市链接跟进
             Rule(LinkExtractor(allow=("http://data.house.sina.com.cn/\w+/search/.*")), follow=True),
             ]
    
    def parse_item(self,response):
        """
        提取具体楼盘信息
        """
        item = SinahouseItem()
        item['house_name'] = response.xpath('/html/body/div[1]/div[9]/div[1]/h2/text()').extract_first().strip()
        item['house_index_url'] = response.url
        item['house_price'] = response.xpath('//*[@id="callmeBtn"]/ul/li[1]/em[1]').extract_first().strip()
        item['house_address'] = response.xpath('//*[@id="callmeBtn"]/ul/li[2]/span[2]').extract_first().strip()
        item['longtitude_latitude'] = [float(response.xpath('//script').re_first(".*?coordx='(\d+.\d+)'")),float(response.xpath('//script').re_first(".*?coordy='(\d+.\d+)'.*"))]
        
        return item