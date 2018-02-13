# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HunterItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    kind = scrapy.Field()
    domain = scrapy.Field()
    url = scrapy.Field()
    snippet = scrapy.Field()
    # line_number = scrapy.Field()
