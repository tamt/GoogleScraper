#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'tamt'

import time
import os
from GoogleScraper import scrape_with_config, GoogleSearchError
# See in the config.cfg file for possible values
config = {
    'SCRAPING': {
        'use_own_ip': 'True',
        'keyword': 'love,test',
        'search_engines': 'sg',
        'num_pages_for_keyword': 1,
        'scrape_method': 'http'
    },
    'GLOBAL': {
        'do_caching': 'False'
    },
    'OUTPUT': {
        'output_filename': os.path.dirname(os.path.realpath(__file__))+"/"+str(time.time())+".json"
    }
}

print(os.path.dirname(os.path.realpath(__file__))+"/"+str(time.time())+".json")

try:
    search = scrape_with_config(config)
except GoogleSearchError as e:
    print(e)
# let's inspect what we got
for serp in search.serps:
    print(serp)
print(serp.search_engine_name)
print(serp.scrape_method)
print(serp.page_number)
print(serp.requested_at)
print(serp.num_results)
# ... more attributes ...
for link in serp.links:
    if link.link_type == "results":
        print(link)