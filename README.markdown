Introduction
------------

**PoE Scrapy** is a Python command line tool made for scraping Path of Exile websites for unique item data.

It was originally built as a proof-of-concept companion tool for updating the unique item data text files used for
[PoE-Item-Info](https://github.com/andreberg/PoE-Item-Info) 

Requirements
------------

[Python 2.7](http://python.org) or later  
[scrapy](http://scrapy.org)

Known Issues
------------

Currently supports only one spider for the main PoE wiki located at pathofexile.gamepedia.com.
However, with scrapy extensibility towards other sites should not be a problem. One can always add a new spider to support other sites.