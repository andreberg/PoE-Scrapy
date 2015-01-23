#!/usr/local/bin/python2.7
# encoding: utf-8
'''
poe_scrape -- scrapy based data scraper

Scrapes PoE web sites for item data.

:author:    | André Berg
:copyright: | 2015 Iris VFX. All rights reserved.
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
:contact:   | andre@irisvfx.com
'''
from __future__ import print_function

import os
import sys

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings

from scrapy_engine.spiders.gamepedia import GamepediaSpider

__all__ = []
__version__ = '0.1'
__date__ = '2015-01-19'
__updated__ = '2015-01-23'

DEBUG = 0 or os.environ.get('DebugLevel', 0)
TESTRUN = 0 or os.environ.get('TestRunLevel', 0)
PROFILE = 0 or os.environ.get('ProfileLevel', 0)

__g_scrapy = None
__g_spiders = [{
    'name': 'gamepedia',
    'target_domain': 'http://pathofexile.gamepedia.com',
    'class': GamepediaSpider
}]


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError, self).__init__()
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg


class Scrapy(object):
    def __init__(self, settings):
        super(Scrapy, self).__init__()
        self.settings = settings
        self.spider = GamepediaSpider()
        self.crawler = Crawler(self.settings)
        self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)  # @UndefinedVariable
        self.crawler.configure()
        self.crawler.crawl(self.spider)

    def get_spider(self):
        return self.spider
    
    def get_crawler(self):
        return self.crawler
    
    def start(self):
        self.crawler.start()
        log.start(loglevel=self.settings.get('LOG_LEVEL', 'INFO'))
        reactor.run() # the script will block here until the spider_closed signal was sent @UndefinedVariable
        
    
def main(argv=None):  # IGNORE:C0111
    if isinstance(argv, list):
        sys.argv.extend(argv)
    elif argv is not None:
        sys.argv.append(argv)
    
    program_name = "poe_scrape"  # IGNORE:W0612 @UnusedVariable
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = '''poe_scrape -- scrapes PoE web sites for item data.'''
    program_license = '''%s
    
  Created by Andre Berg on %s.
  Copyright 2015 Iris VFX. All rights reserved.
  
  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0
  
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))
    
    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument("-i", "--include", dest="include", help="only include URLs matching this regex pattern. Note: exclude is given preference over include. [default: %(default)s]", metavar="RE" )
        parser.add_argument("-e", "--exclude", dest="exclude", help="exclude URLs matching this regex pattern. [default: %(default)s]", metavar="RE" )
        parser.add_argument("-s", "--spider", dest="spider", help="the scrapy spider to run [default: %(default)s]", metavar="NAME" )
        parser.add_argument("-l", "--list-spiders", dest="list_spiders", action='store_true', help="list known spiders and exit")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument('-o', '--outdir', dest="outdir", help="path to output folder [default: %(default)s]", metavar="path")
        
        parser.set_defaults(outdir="output", spider="gamepedia")
        
        # Process arguments
        args = parser.parse_args()
        
        outdir = args.outdir
        verbose = args.verbose
        inpat = args.include
        expat = args.exclude
        spider = args.spider
        list_spiders = args.list_spiders
                
        settings = get_project_settings()
        
        if list_spiders is True:
            spiders_list = ["   {} -> {}".format(s['name'], s['target_domain']) for s in __g_spiders]
            print("List of known spiders: {0}".format(os.linesep))
            print(", ".join(spiders_list))
            return 0
        
        if (spider not in [s["name"] for s in __g_spiders]):
            raise CLIError("Unknown spider: {} (known spiders: {})".format(spider, (", ".join([s["name"] for s in __g_spiders]))))
        
        if inpat and expat and inpat == expat:
            raise CLIError("Include and exclude patterns are equal! Nothing will be processed.")
        
        if verbose > 0:
            print("Verbose mode on")
        
        settings.set("VERBOSE", verbose)

        if DEBUG > 0:
            settings.set("LOG_LEVEL", log.DEBUG)
        else:
            settings.set("LOG_LEVEL", log.INFO)
            
        
        if outdir is None:
            settings.set("OUTPATH", os.curdir)
        else:
            settings.set("OUTPATH", outdir)
        
        if inpat:
            settings.set("INCLUDE_PATTERN", inpat)
        if expat:
            settings.set("EXCLUDE_PATTERN", expat)
        
        global __g_scrapy
        __g_scrapy = Scrapy(settings)
        __g_scrapy.start()
        
        return 0
    except KeyboardInterrupt:
        if (__g_scrapy is not None):
            __g_scrapy.get_crawler().stop()
        return 0
    except CLIError as e:
        print(e)
        return 1
    except Exception as e:
        if DEBUG or TESTRUN:
            raise(e)
        sys.stderr.write("{0}: {1}{2}".format(sys.argv[0].split("/")[-1], str(e), os.linesep))
        sys.stderr.write("\t for help use --help")
        return 2


if __name__ == "__main__":
    '''Command line options.'''
    if DEBUG:
        sys.argv.append("-v")
#         sys.argv.append("-l")
#         sys.argv.append("-s foo")        
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        def profile_tasks():
            main()
        profile_filename = 'scrape-profile.pstats'
        cProfile.run('profile_tasks()', profile_filename)
        statsfile = open("scrape-profile.pstats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        print(stats.print_stats(), file=statsfile)
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
