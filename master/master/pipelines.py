# -*- coding: utf-8 -*-
import re,redis
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class MasterPipeline(object):
    def __init__(self, host, port):
        self.r = redis.Redis(host=host, port=port, decode_responses=True)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
                host = crawler.settings.get('REDIS_HOST'),
                port = crawler.settings.get('REDIS_PORT')
            )

    #用itempipeline过滤掉url
    def process_item(self, item, spider):
        #使用正则判断url地址是否有效，并写入Redis
        bookid = re.findall('book.douban.com/subject/([0-9]+)/', item['url'])
        if bookid:
            if self.r.sadd('books:id',bookid[0]):
                self.r.lpush('bookspider:start_urls', item['url'])
        else:
            self.r.lpush('bookspider:no_urls', item['url'])
        
