# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from crawlerA.items import bgmtvItem, bgmtvcharacterItem, bgmtvpersonsItem

year,page,where = (1985, 1, 1)

class BgmtvSpider(scrapy.Spider):
    name = 'bgmtv'
    allowed_domains = ['bgm.tv']
    start_urls = [f'https://bgm.tv/anime/browser/airtime/{year}']

    def parse(self, response):
        # 遍历page读取单subject的url
        licount = len(response.xpath('//*[@id="browserItemList"]/li'))
        # 可能存在白页
        if licount:
            for _ in range(1, licount+1):
                where = _
                li = response.xpath(f'//*[@id="browserItemList"]/li[{_}]')
                try:
                    # 存在评价的权重 才有爬取价值
                    test = li.xpath('//p[@class="rateInfo"]/small')
                    subject_url = 'https://bgm.tv'+li.xpath('//a/@href').extract()[0]
                    title = li.xpath('//a/text()').extract()[0]
                    self.logger.info('[索引]爬取 < %s > 现在位置：(%s,%s,%s)',title,year,page,where)
                    # /subject/xxxx
                    yield scrapy.Request(subject_url, callback=self.parse_subject)
                except:
                    continue
                
        # 翻页
        if '››' in response.xpath('//a[@class = "p"]/text()').extract():
            # ["1", "2", ... ,">>",">|"]
            page = page + 1
            self.logger.info('[索引]下一页 现在位置：(%s,%s,%s)',year,page,where) 
        else:
            # 爬取下一年
            year = year + 1
            page = 1
            self.logger.info('[索引]下一年 现在位置：(%s,%s,%s)',year,page,where)
        nexturl = f'https://bgm.tv/anime/browser/airtime/{year}?page={page}'
        yield scrapy.Request(nexturl, callback=self.parse)
        
    def parse_subject(self, response):
        if response.xpath('//*[@id="colunmNotice"]'):
            # 404 可能爬到里区
            self.logger.warn('[页面subject] 404 可能爬到里区 %s ',response.url)
            return
        
        bgmtv_subject = bgmtvItem()

        bgmtv_subject['namesingle'] = response.xpath('//*[@id="headerSubject"]/h1/a/text()').extract()[0]
        bgmtv_subject['pageurl'] = response.xpath('//*[@id="headerSubject"]/h1/a/@herf').extract()[0]


        bgmtv_subject['coverimg'] = response.xpath('//*[@id="bangumiInfo"]/div/div[1]/a/@herf').extract()[0]
        # img download?
        bgmtv_subject['infobox'] = response.xpath(f'//*[@id="infobox"]/li').extract()
        bgmtv_subject['watchcont'] = response.xpath('//*[@id="subjectPanelCollect"]/span/a/text()').extract()

        bgmtv_subject['eps'] = response.xpath('//*[@id="subject_detail"]/div[1]/ul/li').extract()
        bgmtv_subject['eps_content'] = response.xpath('//*[@id="subject_prg_content"]/div').extract()
        
        bgmtv_subject['summary'] = response.xpath('//*[@id="subject_summary"]/text()').extract()[0]
        bgmtv_subject['tag_section'] = response.xpath('//*[@id="subject_detail"]/div[3]/div/a').extract()
        bgmtv_subject['chara'] = response.xpath('//*[@id="browserItemList"]/li')

        bgmtv_subject['aboutsubject'] = response.xpath('//*[@id="columnSubjectHomeB"]/div[3]/div[2]/ul/li')
        bgmtv_subject['maybelike'] = response.xpath('//*[@id="columnSubjectHomeB"]/div[4]/div/ul/li')

        bgmtv_subject['global_score'] = response.xpath('//*[@class="global_score"]/text()').extract()[0]
        bgmtv_subject['memberrating'] = response.xpath('//*[@id="ChartWarpper"]/text()').extract()[0]

        # 全部解析完成，开始解析扩展信息，数据库建立新文档
        yield scrapy.Request(response.url+'/characters', callback=self.parse_characters)
        yield scrapy.Request(response.url+'/persons', callback=self.parse_persons)

        yield bgmtv_subject
        self.logger.info('[页面subject] 初加工完成 %s | < %s >',bgmtv_subject['namesingle'],response.url)

    def parse_characters(self, response):
        charapage = bgmtvcharacterItem()
        charapage['characters'] = response.xpath('//*[@id="columnInSubjectA"]/div')
        yield charapage

    def parse_persons(self, response):
        pspage = bgmtvpersonsItem()
        pspage['persons'] = response.xpath('//*[@id="columnInSubjectA"]/div')
        yield pspage
