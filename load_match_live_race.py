#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-01-18 19:52:55
# Project: load_match_live_race

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
        'Content-Type': 'application/json',  
    }

def getCookie():
    return {
        "uid": "R-563407-3387d81805e23c6c2f1e24",
        "ds_session": "b2p49bqf6db0ds064k64f4pl85",
        "halfbt_daxiao": "1",
        "halfbt_rangfen": "1",
        "race_id": "561883",
    }
    


class Handler(BaseHandler):
    crawl_config = {
        'proxy':"HZ66310Z7I39EY4P:1CCD8C4876D5635C@http-pro.abuyun.com:9010",
    }
    
    
    def on_start(self):
        self.crawl('https://www.dszuqiu.com/', callback=self.index_page, validate_cert=False, headers=get_headers(), cookies=random_bid())

    
    def index_page(self, response):
        start = "2019-01-01"
        end = "2019-01-01"
        
        match_list_res = requests.get("http://local.ds.football/api/match/getMatchByDate?startDate="+start+"&endDate="+end)

        match_list = json.loads(match_list_res.content)

        for match_id in match_list:
            self.crawl("https://www.dszuqiu.com/race_sp/"+str(match_id), callback=self.detail_page, validate_cert=False, headers=get_headers(), cookies=getCookie())
  
    @config(priority=2)
    def detail_page(self, response):
        bs_halt_data = []
        bs_full_data = []
        wd_halt_data = []
        wd_full_data = []
        
        match_id = response.url[8:].split('/')[-1]

        #大小球半场
        for tr in response.doc("div[class='small-4 columns tableCol3in1 daxiao']").find("table[class='responsive half'] > tbody").items("tr"):
            match_time = tr.children("td").eq(0).text()[:-1]
            score = tr.children("td").eq(1).text()
            big = tr.children("td").eq(2).text()
            bsp = tr.children("td").eq(3).text()
            small = tr.children("td").eq(4).text()
            date_time = tr.children("td").eq(5).text()
            _type = 0
            
            live_data = {
                "match_id": match_id,
                "match_time": match_time,
                "score": score,
                "big": big,
                "small": small,
                "bsp": bsp,
                "date_time": date_time,
                "type": _type 
            }
            
            bs_halt_data.append(live_data)

        #大小球全场
        for tr in response.doc("div[class='small-4 columns tableCol3in1 daxiao']").find("table[class='responsive full'] > tbody").items("tr"):
            match_time = tr.children("td").eq(0).text()[:-1]
            score = tr.children("td").eq(1).text()
            big = tr.children("td").eq(2).text()
            bsp = tr.children("td").eq(3).text()
            small = tr.children("td").eq(4).text()
            date_time = tr.children("td").eq(5).text()
            _type = 1
            
            live_data = {
                "match_id": match_id,
                "match_time": match_time,
                "score": score,
                "big": big,
                "small": small,
                "bsp": bsp,
                "date_time": date_time,
                "type": _type 
            }
            
            bs_full_data.append(live_data)

        #胜平负半场
        for tr in response.doc("div[class='small-4 columns tableCol3in1 wincast']").find("table[class='responsive half'] > tbody").items("tr"):
            match_time = tr.children("td").eq(0).text()[:-1]
            score = tr.children("td").eq(1).text()
            win = tr.children("td").eq(2).text()
            let_ball = tr.children("td").eq(3).text()
            lose = tr.children("td").eq(4).text()
            date_time = tr.children("td").eq(5).text()
            _type = 0
            
            live_data = {
                "match_id": match_id,
                "match_time": match_time,
                "score": score,
                "win": win,
                "let_ball": let_ball,
                "lose": lose,
                "date_time": date_time,
                "type": _type 
            }
            
            wd_halt_data.append(live_data)


        #胜平负全场
        for tr in response.doc("div[class='small-4 columns tableCol3in1 wincast']").find("table[class='responsive full'] > tbody").items("tr"):
            match_time = tr.children("td").eq(0).text()[:-1]
            score = tr.children("td").eq(1).text()
            win = tr.children("td").eq(2).text()
            let_ball = tr.children("td").eq(3).text()
            lose = tr.children("td").eq(4).text()
            date_time = tr.children("td").eq(5).text()
            _type = 1
            
            live_data = {
                "match_id": match_id,
                "match_time": match_time,
                "score": score,
                "win": win,
                "let_ball": let_ball,
                "lose": lose,
                "date_time": date_time,
                "type": _type 
            }
            
            wd_full_data.append(live_data)

        #要保存的数据
        post_data = {
            "bs_halt_data": json.dumps(bs_halt_data),
            "bs_full_data": json.dumps(bs_full_data),
            "wd_halt_data": json.dumps(wd_halt_data),
            "wd_full_data": json.dumps(wd_full_data)
        }
        
        insert_res = requests.post("http://local.ds.football/api/match/live/store", data=post_data)    

        return { match_id: json.loads(insert_res.content) }
            
        
