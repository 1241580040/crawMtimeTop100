# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Crawmtimetop100Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    name = scrapy.Field()
    addr = scrapy.Field()
    picCount = scrapy.Field()
