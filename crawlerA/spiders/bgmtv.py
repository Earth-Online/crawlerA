# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from crawlerA.items import bgmtvItem

class BgmtvSpider(scrapy.Spider):
    name = 'bgmtv'
    allowed_domains = ['bgm.tv']
    start_urls = ['https://bgm.tv/']

    def parse(self, response):
        # 未确定索引目录

        # 遍历页面读取单subject的url
        count = len(response.xpath(''))
        for _ in range(count):
            subject_url = response.xpath('')
            yield scrapy.Request(subject_url, callback=self.parse_subject)

        # 翻页行为
        nexturl = response.xpath('')
        self.logger.info('下一页：%s', nexturl)
        if nexturl:
            yield scrapy.Request(nexturl, callback=self.parse)
        
    def parse_subject(self, response):
        bgmtv_subject = bgmtvItem()

        namesingle = response.xpath('//*[@id="headerSubject"]/h1/a/text()')
        pageurl = response.xpath('//*[@id="headerSubject"]/h1/a/@herf')
        # url split
        coverimg = response.xpath('//*[@id="bangumiInfo"]/div/div[1]/a')
        # img download?
        infobox = response.xpath('//*[@id="infobox"]')
        # TODO list
        watchcont = response.xpath('//*[@id="subjectPanelCollect"]/span')
        # TODO split
        eps = response.xpath('//*[@id="subject_detail"]/div[1]/ul')
        eps_content = response.xpath('//*[@id="subject_prg_content"]')
        # TODO list split remove
        summary = response.xpath('//*[@id="subject_summary"]/text()')
        tag_section = response.xpath('//*[@id="subject_detail"]/div[3]/div')
        # TODO list split
        chara = response.xpath('//*[@id="browserItemList"]')
        # TODO list split remove img
        aboutsubject = response.xpath('//*[@id="columnSubjectHomeB"]/div[3]/div[2]/ul')
        # TODO list split remove img 
        maybelike = response.xpath('//*[@id="columnSubjectHomeB"]/div[4]/div/ul')
        # TODO list split remove img
        rating = response.xpath('//*[@id="panelInterestWrapper"]/div[1]/div')
        # TODO list split remove

        # 全部解析完成，开始解析扩展信息，数据库建立新文档
        yield bgmtv_subject
        self.logger.info('%s|%s 解析完成',namesingle,pageurl)
        yield scrapy.Request(response.url+'/characters', callback=self.parse_characters)
        yield scrapy.Request(response.url+'/persons', callback=self.parse_persons)

    def parse_characters(self, response):
        characters = response.xpath('//*[@id="columnInSubjectA"]')
        # TODO list split

    def parse_persons(self, response):
        persons = response.xpath('//*[@id="columnInSubjectA"]')
        # TODO list split