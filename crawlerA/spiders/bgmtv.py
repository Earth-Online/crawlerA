# -*- coding: utf-8 -*-
import scrapy


class BgmtvSpider(scrapy.Spider):
    name = 'bgmtv'
    allowed_domains = ['bgm.tv']
    start_urls = ['https://bgm.tv/']

    def parse(self, response):
        pass
