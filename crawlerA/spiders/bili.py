# -*- coding: utf-8 -*-
import scrapy
from crawlerA.items import biliItem

class BiliSpider(scrapy.Spider):
    name = 'bili'
    allowed_domains = ['bilibili.com']
    start_urls = ['https://www.bilibili.com/anime/index/#season_version=-1&area=2&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&pub_date=-1&style_id=-1&order=3&st=1&sort=0&page=1']

    def parse(self, response):
        # 遍历页面读取单media的url
        count = len(response.xpath('//*[@id="app"]/div[2]/div[1]/ul[2]/li'))
        for _ in range(1, count+1):
            media_tab = response.xpath(f'//*[@id="app"]/div[2]/div[1]/ul[2]/li[{count}]')
            href = media_tab.xpath('//a/@href').extract()[0]
            # href="//www.bilibili.com/bangumi/play/ ss 24588/"
            media_url = 'https://www.bilibili.com/bangumi/media/md'+href.split('ss')
            yield scrapy.Request(media_url, callback=self.parse_media)

        # 翻页行为 坑爹的js翻页。。。
        # https://www.bilibili.com/anime/index/#seas...ort=0& page= 2
        _ = response.url.split('page=')
        nexturl = _[0]+'page='+str(int(_[1])+1)
        
        self.logger.info('[索引]下一页 %s', nexturl)
        yield scrapy.Request(nexturl, callback=self.parse)

    def parse_media(self, response):
        bangumi = biliItem()

        bangumi['pageurl'] = response.url
        
        bangumi['img'] = response.xpath('//*[@id="app"]/div[1]/div[2]/div/div[1]/div/img/@src').extract()[0]
        bangumi['title'] = response.xpath('//*[@id="app"]/div[1]/div[2]/div/div[2]/div[1]/span[1]/text()').extract()[0]
        bangumi['tags'] = response.xpath('//*[@id="app"]/div[1]/div[2]/div/div[2]/div[1]/span[2]/span/text()').extract()
        bangumi['bigdata'] = response.xpath('//*[@id="app"]/div[1]/div[2]/div/div[2]/div[2]/div[1]/text()').extract()[0]
        bangumi['rating'] = response.xpath('//*[@id="app"]/div[1]/div[2]/div/div[2]/div[2]/div[2]/text()').extract()[0]
        bangumi['time'] = response.xpath('//*[@id="app"]/div[1]/div[2]/div/div[2]/div[3]/span[1]/text()').extract()[0]
        bangumi['eps'] = response.xpath('//*[@id="app"]/div[1]/div[2]/div/div[2]/div[3]/span[2]/text()').extract()[0]
        bangumi['intro'] = response.xpath('//*[@id="app"]/div[1]/div[2]/div/div[2]/div[4]/span/text()').extract()[0]

        # 声优演员与staff
        smallbox = response.xpath('//*[@id="app"]/div[2]/div[2]/div/div[2]/div')
        if smallbox:
            # 白页可能
            for onebox in smallbox:
                if '角色' or '声优' in onebox.xpath('//div[1]/text()').extract()[0]:
                    bangumi['cast'] = onebox.xpath('//div[2]/text()').extract()[0]
                elif 'STAFF' in onebox.xpath('//div[1]/text()').extract()[0]:
                    bangumi['staff'] = onebox.xpath('//div[2]/text()').extract()[0]
                else:
                    self.logger.warn('[页面media] %s 标题不合法',bangumi['pageurl'])

        yield bangumi
        self.logger.info('[页面media] 初加工完成 %s | < %s >',bangumi['title'],bangumi['pageurl'])
