# -*- coding: utf-8 -*-

# Scrapy settings for scrapy_engine project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scrapy_engine'

SPIDER_MODULES = ['scrapy_engine.spiders']
NEWSPIDER_MODULE = 'scrapy_engine.spiders'

ITEM_PIPELINES = {
    'scrapy_engine.pipelines.PoeScrapyPipeline': 300
}

CONCURRENT_REQUESTS_PER_DOMAIN = 4
CONCURRENT_REQUESTS = 4
CONCURRENT_ITEMS = 10
ROBOTSTXT_OBEY = True

# Append "; <item url>" as line terminating comment to Uniques.txt
APPEND_ITEM_URL = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapy_engine (+http://www.yourdomain.com)'
