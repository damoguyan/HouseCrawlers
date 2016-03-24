#!/usr/bin/env python
# coding: utf-8
'''
Created on 2016-03-24

@author: alex
'''
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Request
from house_crawlers.items.lianjiaitem import LianJiaItem

class LianJiaSpider(CrawlSpider):
    """
    链家新房爬虫
    """
    name = 'lianjia'
    allowed_domains = ['fang.lianjia.com']
    start_urls = ['http://sh.fang.lianjia.com/',]
    rules = [
             #各城市链接跟进
             Rule(LinkExtractor(allow=('^http://\w+.fang.lianjia.com/loupan/$')), callback='parse_next_url', follow=True),
             #具体楼盘链接跟进
             Rule(LinkExtractor(allow=('^http://\w+.fang.lianjia.com/loupan/p_\w+/$')), callback='parse_item'),
             
             ]
    
    def parse_next_url(self,response):
        totalpage = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').re_first('.*?"totalPage":(\d+),.*')
        totalpage = int(totalpage if totalpage else 1)
        #http://\w+.fang.lianjia.com/loupan/
        url = response.url + 'pg%s/'
        for i in range(1, totalpage):
            yield Request(url % i)
    
    def parse_item(self,response):
        item = LianJiaItem()
        item['house_name'] = response.xpath('//div[@class="name-box"]/a/h1/text()').extract_first().strip()
        item['house_index_url'] = response.url
        item['house_price'] = ''.join(response.xpath('//p[@class="jiage"]/span[not(@title)]/text()').extract())
        item['house_address'] = response.xpath('//p[@class="where"]/span/text()').extract_first()
        item['longtitude_latitude'] = ','.join(response.xpath('//*[@id="mapWrapper"]/@data-coord').extract_first().split(',')[::-1])
        return item
        