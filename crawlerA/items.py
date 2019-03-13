# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnimeItem(scrapy.Item):
    # 动画信息
    dbindex = scrapy.Field()
    origin_url = scrapy.Field()

    # 基本信息
    name = scrapy.Field()
    cover = scrapy.Field()
    time = scrapy.Field()
    eps =  scrapy.Field()

    # 类型 故事简介
    genre = scrapy.Field()
    story = scrapy.Field()

    # 需演员员工索引信息扩展
    cast = scrapy.Field()
    staff = scrapy.Field()

    # 评测数据
    label = scrapy.Field()
    ranking = scrapy.Field()

    # 需要更多数据
    # streaming
    # recommend
    # relate

class CastItem(scrapy.Item):
    # 角色演员对应
    dbindex = scrapy.Field()
    origin_url = scrapy.Field()
    castdict = scrapy.Field()

class StaffItem(scrapy.Item):
    # 仕事人员与岗位对应
    dbindex = scrapy.Field()
    origin_url = scrapy.Field()
    staffdict = scrapy.Field()
