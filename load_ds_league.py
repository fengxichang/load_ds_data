#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-01-01 20:47:33
# Project: Load_DS_data
# 从ds足球爬取联赛数据

from pyspider.libs.base_handler import *
import datetime
import requests
import json
import time
import random
import string
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

#生成随机请求头
def gen_headers():
    return { 
        'User-Agent': random_agent(),
        "Host": "www.dszuqiu.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "zh-CN, zh; q=0.8, en; q=0.6",
    }


def random_bid():
    #return {'bid': 'MC2U0Nf8TdZ'}
    return {'bid': ''.join(random.sample(string.ascii_letters + string.digits, 11))}


class Handler(BaseHandler):
    crawl_config = {
       'proxy':"HZ66310Z7I39EY4P:1CCD8C4876D5635C@http-pro.abuyun.com:9010"
    }
    
  
    def on_start(self):
        self.crawl('https://www.dszuqiu.com/data', callback=self.index_page, validate_cert=False, headers=gen_headers(), cookies=random_bid())

   
    def index_page(self, response):
        continent_list = ['panel2-0','panel2-1','panel2-2','panel2-3','panel2-4','panel2-5']
        for id in continent_list:
            for li in response.doc('section[id='+id+']').find('ul[class="dataListCon2"]').items('li'):
                href = li.find('a').attr('href') 
                self.crawl(href, callback=self.detail_page, validate_cert=False, headers=gen_headers(), cookies=random_bid())
                

    def detail_page(self, response):
        
        h1 = response.doc('h1[class="titleL1 BB0"]')
        namestr = h1.text()[3:].split('，')
        
        league_id = response.url[8:].split('/')[-1]
        name = namestr[0]
        alias = namestr[1]
        desc = response.doc('p[class="f14"]').text()
        league_type = h1.text()[0:2]
        
        league_data = {
            "id": league_id,
            "name": name,
            "alias": alias,
            "desc": desc,
            "type": league_type
        }
        
        insert_response = requests.post("http://ds.football.cn/api/league/store", league_data)

        return { "league_id":league_id, "result":json.loads(insert_response.content) }