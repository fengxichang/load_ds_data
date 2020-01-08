#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-01-05 13:12:52
# Project: ds_load_team
# 爬取ds足球球队数据

from pyspider.libs.base_handler import *
import datetime
import requests
import json
import time
import random
import string

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
def get_headers():
    return {
        "User-Agent": random_agent(),
        "Host": "www.dszuqiu.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0,image/webp,*/*;q=0.8",
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
        self.crawl('https://www.dszuqiu.com', callback=self.index_page, validate_cert=False, headers=get_headers(), cookies=random_bid())

    def index_page(self, response):
        league_list_res = requests.get('http://local.ds.football/api/league/getList')
        
        league_list = json.loads(league_list_res.content)
        
        for league_id in league_list:
            self.crawl('www.dszuqiu.com/league/'+ str(league_id), callback=self.detail_page, validate_cert=False, headers=get_headers(), cookies=random_bid())
            
            

    def detail_page(self, response):
        
        if not response.doc('table[class="responsive MB0 live-list-table"]'):
            return {response.url:None}
        
        result = {}
        
        for tr in response.doc('table[class="responsive MB0 live-list-table"]').find('tbody').items('tr'):
            cn_name = tr.children('td').eq(2).children('a').text()
            team_id = tr.children('td').eq(2).children('a').attr('href').split('/')[-1]
            team_data = {
                "id": team_id,
                "cn_name": cn_name
            }
            
            insert_response = requests.post("http://local.ds.football/api/team/store", team_data)
            result.update({team_id:json.loads(insert_response.content)})
        
        return result