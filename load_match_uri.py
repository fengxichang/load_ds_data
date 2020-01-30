#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-01-12 10:52:55
# Project: load_match_base

from pyspider.libs.base_handler import *
import time,datetime
import random
import string
import requests
import json

def random_agent():
    user_agent_list = [\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
       ]
    return random.choice(user_agent_list)


def random_bid():
    return { "bid": "".join(random.sample(string.ascii_letters + string.digits, 11)) }


def get_headers():
    return {
        "User-Agent": random_agent(),
        "Host": "www.dszuqiu.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "zh-CN, zh; q=0.8, en; q=0.6",
        'Content-Type': 'application/json'
    }


class Handler(BaseHandler):
    crawl_config = {
        'proxy':"HZ66310Z7I39EY4P:1CCD8C4876D5635C@http-pro.abuyun.com:9010"
    }
    
    
    def on_start(self):
        self.crawl('https://www.dszuqiu.com/', callback=self.index_page, validate_cert=False, headers=get_headers(), cookies=random_bid())

    
    def index_page(self, response):
        start = "2017-01-01"
        end = "2019-12-31"
        
        dateStart = datetime.datetime.strptime(start,"%Y-%m-%d")
        dateEnd = datetime.datetime.strptime(end, "%Y-%m-%d")
        
        while dateStart <= dateEnd:
            self.crawl("https://www.dszuqiu.com/diary/"+ dateStart.strftime('%Y%m%d'), callback=self.detail_page, validate_cert=False, headers=get_headers(), cookies=random_bid())
            dateStart += datetime.timedelta(days=1)
  
    @config(priority=2)
    def detail_page(self, response):
        result = {}
        data_list = []
        match_date = datetime.datetime.strptime(response.url[8:].split('/')[-1], "%Y%m%d").strftime('%Y-%m-%d')
        
        if (not response.doc("div[class='pagination-centered']").children("ul")):
            data_list.append(response.url)
        else:
            for li in response.doc("div[class='pagination-centered']").children("ul").items("li"):
            
                match_url = li.children("a").attr("href")

                data_list.append(match_url)
            
        insert_res = requests.post("http://ds.football.cn/api/match/matchUriStore", data={"url_list":json.dumps(data_list), "date":match_date}) 
           
        return { match_date: json.loads(insert_res.content) }
            
        
