# -*- coding: utf-8 -*-
import scrapy,redis 
from urllib.parse import quote
from scrapy import Request
from master.items import MasterItem

class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['book.douban.com']
    base_url = 'https://book.douban.com'

    def start_requests(self):
        #设置Redis数据库信息
        r = redis.Redis(host=self.settings.get('REDIS_HOST'),port=self.settings.get('REDIS_PORT'),decode_responses=True)
        while r.llen('book:tag_urls'):
            tag = r.lpop('book:tag_urls')
            url = self.base_url + quote(tag)
            yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        #解析每页图书的详情信息
        print(response.url)
        items = response.css('#subject_list .subject-item .info a::attr(href)').extract()
        if items:
            for i in items:
                item = MasterItem()
                item['url'] = i
                yield item

        #获取下一页的url地址
        next = response.css('.next a::attr(href)').extract_first()
        if next:
            url = response.urljoin(next)
            yield scrapy.Request(url=url, callback=self.parse )
