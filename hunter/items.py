# -*- coding: utf-8 -*-

import scrapy


class HunterItem(scrapy.Item):
    title = scrapy.Field()
    kind = scrapy.Field()
    domain = scrapy.Field()
    url = scrapy.Field()
    snippet = scrapy.Field()
