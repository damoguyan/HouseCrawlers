#!/usr/bin/env python
# coding: utf-8
'''
Created on 2016-03-21

@author: alex
'''

from twisted.enterprise import adbapi

class MySQLPipeline(object):
    '''
    数据写入 mysql的管道
    '''
    def __init__(self, logger, stats, mysql_info):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **mysql_info)
        self.stats = stats
        self.logger = logger
        
    @classmethod
    def from_crawler(cls, crawler):
        '''
        获取数据库连接信息
        '''
        mysql_info = crawler.settings.get('MYSQL_INFO')
        stats = crawler.stats
        logger = crawler.logger
        return cls(logger, stats, mysql_info)
        
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.__insert, item)
        query.addErrback(self._handle_error)
        return item
    
    def _insert(self, tx, item):
        result = tx.execute(""" 
        insert into table house_info(house_name,house_index_url,house_price,house_address,longtitude_latitude)
        values (%s,%s,%s,%s,%s)""",(item['house_name'],item['house_index_url'],item['house_price'],item['house_address'],item['longtitude_latitude']))
        
        if result > 0:
            self.stats.inc_value('mysql_items_added', count=1, start=0)
        
    def _handle_error(self,e):
        self.logger.error(e)