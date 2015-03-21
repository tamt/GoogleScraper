#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

__author__ = 'tamt'

import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import io
import shutil
import urllib

from GoogleScraper import scrape_with_config, GoogleSearchError, Config


all_search_engines = [se.strip() for se in Config['SCRAPING'].get('supported_search_engines').split(',')]


class MyHttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        currtime = str(time.time()).split(".")[0]
        if '?' in self.path:
            self.queryString = urllib.parse.unquote(self.path.split('?', 1)[1])
            params = urllib.parse.parse_qs(self.queryString)
            if ('query' in params) and ('lang' in params) and ('pages' in params):
                query = params['query'][0]
                lang = params['lang'][0]
                pages = params['pages'][0]
                opfile = currtime + '.txt'

                keywordfile = open(currtime + '.keyword', 'w', encoding='utf-8')
                lines = [line + '\n' for line in query.split(',')]
                keywordfile.writelines(lines)
                keywordfile.close()

                num_workers = len(lines)
                if num_workers > 10:
                    num_workers = 10
                print('使用线程数：' + str(num_workers))

                if lang in all_search_engines:

                    # See in the config.cfg file for possible values
                    config = {
                        'SCRAPING': {
                            'use_own_ip': 'True',
                            'keyword_file': keywordfile.name,
                            'search_engines': lang,
                            'num_pages_for_keyword': pages,
                            'num_workers': num_workers,
                            'scrape_method': 'http'
                        },
                        'GLOBAL': {
                            'do_caching': 'False'
                        },
                        'OUTPUT': {
                            'output_filename': os.path.dirname(os.path.realpath(__file__))+"\\"+opfile
                        }
                    }

                    print(os.path.dirname(os.path.realpath(__file__))+"\\"+opfile)

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
                            if link.link_type != 'ads_main':
                                print(link)

                    r_str = opfile
                    os.remove(keywordfile.name)
                else:
                    r_str = "[error]不支持的语言：" + lang
            else:
                r_str = "[error]参数不对：" + self.queryString
        else:
            r_str = Config['SCRAPING'].get('supported_search_engines')

        enc = "UTF-8"
        encoded = ''.join(r_str).encode(enc)
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)


port = 1111
httpd = HTTPServer(('', port), MyHttpHandler)
print("Server started on 127.0.0.1,port " + str(port) + ".....")
httpd.serve_forever()