# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UniqueItemsList(scrapy.Item):
    '''
    Represents a list of unique items, e.g. a 
    list of unique items on gamepedia.com, like
    http://pathofexile.gamepedia.com/List_of_unique_boots
    '''
    list_title = scrapy.Field()
    entry = scrapy.Field()
    all_names = scrapy.Field()
    all_mods = scrapy.Field()
    
class UniqueItem(scrapy.Item):
    '''
    Represents a unique item from a unique item list.
    '''
    name = scrapy.Field()
    implicit_mods = scrapy.Field()
    affix_mods = scrapy.Field() 
    url = scrapy.Field()
    category = scrapy.Field()
    