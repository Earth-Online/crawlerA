# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# rawdata 生数据

class bgmtvItem(scrapy.Item):
    pageurl = scrapy.Field()
    namesingle = scrapy.Field()
    coverimg = scrapy.Field()
    infobox = scrapy.Field()
    watchcont = scrapy.Field()

    eps = scrapy.Field()
    eps_content = scrapy.Field()

    summary = scrapy.Field()
    tag_section = scrapy.Field()

    chara = scrapy.Field()
    aboutsubject = scrapy.Field()
    maybelike = scrapy.Field()
    rating = scrapy.Field()

class bgmtvcharacterItem(scrapy.Item):
    character = scrapy.Field()

class bgmtvpersonsItem(scrapy.Item):
    persons = scrapy.Field()

class biliItem(scrapy.Item):
    pageurl = scrapy.Field()
    img = scrapy.Field()
    title = scrapy.Field()
    tags = scrapy.Field()
    bigdata = scrapy.Field()
    rating = scrapy.Field()
    time = scrapy.Field()
    eps = scrapy.Field()
    intro = scrapy.Field()

    cast = scrapy.Field()
    staff = scrapy.Field()

class pptvItem(scrapy.Item):
    pass

class dongasiteItem(scrapy.Item):
    pass