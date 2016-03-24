#!/usr/bin/env python
# coding: utf-8
'''
Created on 2016-03-22

@author: alex
'''
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from house_crawlers.items.anjukeitem import AnjukeItem

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
             Rule(LinkExtractor(allow=('^http://\w+.fang.anjuke.com/loupan/s\?p=\d+$')),follow=True),
             #楼盘详情页
             Rule(LinkExtractor(allow=('^http://\w+.fang.anjuke.com/loupan/\d+.html$')),callback="parse_item"),
             ]
    def parse_item(self, response):
        item = AnjukeItem()
        item['house_name'] = response.xpath('//*[@id="j-triggerlayer"]/text()').extract_first().strip()
        item['house_index_url'] = response.url
        item['house_price'] = response.xpath('//*[@id="container"]//dd[@class="price"]/p/text()[1]').extract_first(default='').strip()+\
            response.xpath('//*[@id="container"]//dd[@class="price"]/p/em/text()').extract_first(default='').strip() +\
            response.xpath('//*[@id="container"]//dd[@class="price"]/p/text()[2]').extract_first(default='').strip()
        item['house_address'] = response.xpath('//*[@id="container"]//span[@class="lpAddr-text"]/text()').extract_first()
        item['longtitude_latitude'] = response.xpath('//script').re_first('.*?lng: (\d+.\d+)') + ',' + response.xpath('//script').re_first('.*?lat: (\d+.\d+)')
        return item
        