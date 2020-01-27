#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-01-21 20:52:55
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
        #"Hm_lvt_a68414d98536efc52eeb879f984d8923": "1579348840,1579402940",
        #"Hm_lpvt_a68414d98536efc52eeb879f984d8923": "1579403944"
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
            self.crawl("https://www.dszuqiu.com/race_ss/"+str(match_id), callback=self.detail_page, validate_cert=False, headers=get_headers(), cookies=getCookie())
  
    @config(priority=2)
    def detail_page(self, response):
        match_history_data = []
        history_against_id = []
        home_lately_match_id = []
        visit_lately_match_id = []
        
        c = response.url[8:].split('/')[-1]

        divs = response.doc("div[class='small-12 medium-12 columns']").items("div[class='panel panel-l']")
        print(len(divs))

        for div in divs:
            if div.children("div[class='panel-heading']").find("h3").text()=="双方对战历史详情":

                #双方交战历史记录
                for tr in div.children("tbody").items("tr"):
                    history_against_id.append(tr.children("td").eq(10).children("a").attr("href").split("/")[-1])

            elif div.children("div[class='panel-heading']").find("h3").text()=="双方历史比赛统计":
                
                #比赛历史数据
                for tr in div.children("div[id='history1']").find("tbody").items("tr"):
                        #主队最近比赛
                        home_lately_match_id.append(tr.children("td").eq(11).children("a").attr("href").split("/")[-1])

                for tr in div.children("div[id='history2']").find("tbody").items("tr"):
                        #客队最近比赛
                        visit_lately_match_id.append(tr.children("td").eq(11).children("a").attr("href").split("/")[-1])

                tbody = div.children("div[id='history_table']").children("tbody")

                #主队历史比赛数据
                home_match_history_data_tmp = {
                    "match_id": match_id,
                    "team_id": response.doc("h3[class='analysisTeamName red-color']").children("a").attr("href").split("/")[-1],
                    "lately": 6,
                    "type": 1,
                    "only_this_league": 0,
                    "goal_halt": tbody.children("tr").eq(0).children("td").eq(2).text().split("/")[0],
                    "goal_full": tbody.children("tr").eq(0).children("td").eq(2).text().split("/")[-1],
                    "concede_half": tbody.children("tr").eq(0).children("td").eq(3).text().split("/")[0],
                    "concede_full": tbody.children("tr").eq(0).children("td").eq(3).text().split("/")[-1],
                    "big_rate": tbody.children("tr").eq(0).children("td").eq(4).text(),
                    "win_position_rate": tbody.children("tr").eq(0).children("td").eq(5).text(),
                    "win_rate": tbody.children("tr").eq(0).children("td").eq(6).text(),
                    "goal_difference": tbody.children("tr").eq(0).children("td").eq(7).text(),
                    "total_goal": tbody.children("tr").eq(1).children("td").eq(1).text(),
                    "bsp_half": tbody.children("tr").eq(5).children("td").eq(1).text().split("/")[0],
                    "bsp_full": tbody.children("tr").eq(5).children("td").eq(1).text().split("/")[-1],
                }

                match_history_data.append(home_match_history_data_tmp)

                #客队历史比赛数据
                visit_match_history_data_tmp = {
                    "match_id": match_id,
                    "team_id": response.doc("h3[class='analysisTeamName blue-color']").children("a").attr("href").split("/")[-1],
                    "lately": 6,
                    "type": 0,
                    "only_this_league": 0,
                    "goal_halt": tbody.children("tr").eq(2).children("td").eq(2).text().split("/")[0],
                    "goal_full": tbody.children("tr").eq(2).children("td").eq(2).text().split("/")[-1],
                    "concede_half": tbody.children("tr").eq(2).children("td").eq(3).text().split("/")[0],
                    "concede_full": tbody.children("tr").eq(2).children("td").eq(3).text().split("/")[-1],
                    "big_rate": tbody.children("tr").eq(2).children("td").eq(4).text(),
                    "win_position_rate": tbody.children("tr").eq(2).children("td").eq(5).text(),
                    "win_rate": tbody.children("tr").eq(2).children("td").eq(6).text(),
                    "goal_difference": tbody.children("tr").eq(2).children("td").eq(7).text(),
                    "total_goal": tbody.children("tr").eq(3).children("td").eq(1).text(),
                    "bsp_half": tbody.children("tr").eq(5).children("td").eq(1).text().split("/")[0],
                    "bsp_full": tbody.children("tr").eq(5).children("td").eq(1).text().split("/")[-1],
                }

                match_history_data.append(visit_match_history_data_tmp)

        #要保存的数据
        post_data = {
            "match_id": match_id,
            "match_history_data": json.dumps(match_history_data),
            "history_against_id": json.dumps(history_against_id),
            "home_lately_match_id": json.dumps(home_lately_match_id),
            "visit_lately_match_id": json.dumps(visit_lately_match_id)
        }
        
        print(post_data)
        
        insert_res = requests.post("http://local.ds.football/api/match/history/store", data=post_data)    

        return { match_id: json.loads(insert_res.content) }
            
        
