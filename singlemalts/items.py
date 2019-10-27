# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinglemaltsItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    region = scrapy.Field()
    distillery = scrapy.Field()
    age = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    number_of_reviews = scrapy.Field()
    tasting_notes = scrapy.Field()
