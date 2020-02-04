#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-02-03 14:52:55
# Project: load_match_base

from pyspider.libs.base_handler import *
import time,datetime
import random
import string
import requests
import json
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

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


def getCookie():
    return {
        "uid": "R-563407-3387d81805e23c6c2f1e24",
        "ds_session": "b2p49bqf6db0ds064k64f4pl85",
        "halfbt_daxiao": "1",
        "halfbt_rangfen": "1",
        "race_id": "561883",
    }
    


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
    
    #@every(minutes=1)
    @config(age=60)
    def on_start(self):
        self.crawl('https://live.dszuqiu.com/', callback=self.index_page,age=60,auto_recrawl=True, validate_cert=False, headers=get_headers(), cookies=random_bid())

    @config(age=60)
    def index_page(self, response):
       
         self.crawl("https://live.dszuqiu.com/ajax/score/data?mt=0&nr=1", cookies=getCookie(), callback=self.detail_page,age=60,auto_recrawl=True, validate_cert=False, headers=get_headers())
        
            

    @config(priority=2)
    def detail_page(self, response):
        star_match_list = []
        
        for match in json.loads(response.content)['rs']:
            try:
                time = int(match['status'])
                
                if time=30:
                    is_star = self.is_star(match)
                    if is_star:
                        star_match_list.append(match)
                        requests.get("https://live.dszuqiu.com/ajax/user/fav/"+match["id"],cookies=getCookie(), verify=False, headers=get_headers())
            except ValueError:
                pass
            
        _res = requests.post("http://local.ds.football/api/match/getLiveMatches", data={"data":json.dumps(star_match_list)})
       
        return { "notice": json.loads(_res.content) }
    
    
    def is_star(self, match):
        
        if float(match['sd']['f']['hdx']) <= 3 and float(match["h_ld"]["dx"][0]["gdxsp"]) <= 1.5 and float(match["h_ld"]["dx"][0]["hdxsp"]) >= 2.5:
            return True
        else:
            return False    
            
        
