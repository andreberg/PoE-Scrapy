# encoding: utf-8
'''
scrapy_engine.spiders.gamepedia -- spider for pathofexile.gamepedia.com

Implements scrapy.Spider for gamepedia.com

:author:    | André Berg
            |
:copyright: | 2015 Iris VFX. All rights reserved.
            |
:license:   | Licensed under the Apache License, Version 2.0 (the "License");
            | you may not use this file except in compliance with the License.
            | You may obtain a copy of the License at
            | 
            | http://www.apache.org/licenses/LICENSE-2.0
            | 
            | Unless required by applicable law or agreed to in writing, software
            | distributed under the License is distributed on an **"AS IS"** **BASIS**,
            | **WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND**, either express or implied.
            | See the License for the specific language governing permissions and
            | limitations under the License.
            |
:contact:   | andre@irisvfx.com
'''
import re
from urlparse import urlparse

import scrapy
from scrapy import Selector, log
from scrapy_engine.items import UniqueItem


class GamepediaSpider(scrapy.Spider):
    
    name = 'gamepedia'
    allowed_domains = ['pathofexile.gamepedia.com']
    encoding = "utf-8"
    start_urls = [
        'http://pathofexile.gamepedia.com/List_of_unique_amulets',
        'http://pathofexile.gamepedia.com/List_of_unique_belts',
        'http://pathofexile.gamepedia.com/List_of_unique_rings',
        'http://pathofexile.gamepedia.com/List_of_unique_quivers',
        'http://pathofexile.gamepedia.com/List_of_unique_body_armours',
        'http://pathofexile.gamepedia.com/List_of_unique_boots',
        'http://pathofexile.gamepedia.com/List_of_unique_gloves',
        'http://pathofexile.gamepedia.com/List_of_unique_helmets',
        'http://pathofexile.gamepedia.com/List_of_unique_shields',
        'http://pathofexile.gamepedia.com/List_of_unique_axes',
        'http://pathofexile.gamepedia.com/List_of_unique_bows',
        'http://pathofexile.gamepedia.com/List_of_unique_claws',
        'http://pathofexile.gamepedia.com/List_of_unique_daggers',
        'http://pathofexile.gamepedia.com/List_of_unique_fishing rods',
        'http://pathofexile.gamepedia.com/List_of_unique_maces',
        'http://pathofexile.gamepedia.com/List_of_unique_staves',
        'http://pathofexile.gamepedia.com/List_of_unique_swords',
        'http://pathofexile.gamepedia.com/List_of_unique_wands',
        'http://pathofexile.gamepedia.com/List_of_unique_life_flasks',
        'http://pathofexile.gamepedia.com/List_of_unique_mana_flasks',
        'http://pathofexile.gamepedia.com/List_of_unique_hybrid_flasks',
        'http://pathofexile.gamepedia.com/List_of_unique_utility_flasks',
        'http://pathofexile.gamepedia.com/List_of_unique_maps'
    ]

    def set_path(self, url_parts):
        doc_path = url_parts.path
        if doc_path.startswith("/"):
            doc_path = doc_path[1:]
        self.path = doc_path

    def get_site_encoding(self):
        return self.encoding
    
    def get_category(self):
        '''List_of_unique_boots -> Boots'''
        path = self.path
        if not path.startswith("List_of_unique"):
            return "Invalid Category"
        last_underscore = path.rfind("_")
        return path[last_underscore+1:].capitalize()
    
    def _is_valid_url(self, url):
        inpat = self._crawler.settings.get('INCLUDE_PATTERN', None)
        expat = self._crawler.settings.get('EXCLUDE_PATTERN', None)
        if expat and re.search(expat, url):
            self.log("Dropping %s (reason: excluded by URL exclude pattern)" % url, level=log.INFO)
            return False
        if inpat and not re.search(inpat, url):
            self.log("Dropping %s (reason: not included by URL include pattern)" % url, level=log.INFO)
            return False
        self.log("Processing %s" % url, level=log.INFO)
        return True

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html
        @url http://pathofexile.gamepedia.com/List_of_unique_XXX
        @scrapes pathofexile.gamepedia.com
        """
        if not self._is_valid_url(response.url):
            return None
        url_parts = urlparse(response.url)
        self.set_path(url_parts)
        #self.log('A response from %s just arrived!' % response.url)
        sel = Selector(response)        
        items = sel.xpath(".//tr[@id]")
        unique_items = []
        for an_item in items: 
            unique_item = UniqueItem()
            unique_item['name'] = an_item.xpath("./td[1]/a[1]/@title").extract()[0]
            num_spans = len(an_item.xpath("./td[last()]//div[@class='itemboxstatsgroup']/span"))
            if num_spans == 1:
                unique_item['implicit_mods'] = []
            else:
                unique_item['implicit_mods'] = an_item.xpath("./td[last()]//div[@class='itemboxstatsgroup'][1]//span/text()").extract()
            affix_mods = an_item.xpath("./td[last()]//div[@class='itemboxstatsgroup'][last()]//span/text()").extract()                
            unique_item['affix_mods'] = affix_mods
            unique_item['url'] = "{}://{}{}".format(url_parts.scheme, 
                                                    url_parts.netloc, an_item.xpath("./td[1]/a[1]/@href").extract()[0])
            unique_item['category'] = self.get_category()
            unique_items.append(unique_item)
        return unique_items
    