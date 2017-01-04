#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-01-04 10:01:56
# Project: demo

import json, time
import logging

from pyspider.libs.base_handler import *

from mysql_wrapper.mysqldb import SQL

logger = logging.getLogger("result")


class Handler(BaseHandler):
    
    headers = {       
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding" : "gzip, deflate, sdch, br",
        "Accept-Language" : "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
        "Cache-Control" : "max-age=0",
        "Connection" : "keep-alive",
        "Host" : "www.zhihu.com",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent" : "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36",

        "Cookie" : '_zap=b1c56d6a-3a23-4049-a041-d2c9217466f1; d_c0="ACCCFGtE5QqPTmn8vPlNBsyyAipIeAdf9oI=|1479964557"; _zap=0a22bc6c-dca7-436d-8ed8-b21d5379f411; login="NDkyMDdmZmI2NzFjNGIxMDk5NGNlYmVhMTA0Njk5Nzc=|1482125609|a62231195958b7534a26af449493a5d05078fb21"; q_c1=8db0b32b5d114aa88f2ebe6042bf901a|1483088422000|1479964557000; _xsrf=43930aba7ac56cc69d6828a0aa9d32b3; l_cap_id="YmUyYjJmYWM5ODVlNDVhZDkxMDBmMjdjYjA0NjhiYjA=|1483497270|f6be6ff009b0e9702307257f7690004101eba966"; cap_id="OGQyMGJjMzQ2ZjdmNDdkZWJkNWVlMmEwMDUxMjVmODU=|1483497270|0edd8251e6a38e68b5b7cbfdfca587a0ab275ae5"; r_cap_id="NTc3YzQ1MGMwMjk0NGE3ODgxOGEzZGYyMjc0NjE0YWU=|1483497271|2291e71f969e6e1c2f35bceb2f7b056aaf0d4b6f"; capsion_ticket="2|1:0|10:1483497493|14:capsion_ticket|44:ZmQ5MmU1OWIzNGJjNGM0ZWEwOWU0OTJlN2E5ZTRiOWU=|90482abd80bb32e46a7364706de070d7afc3f34b16e432045bbf6ace9b270553"; s-q=%E7%9F%A5%E4%B9%8E%20%E7%88%AC%E8%99%AB; s-i=5; sid=5g0iuc82; z_c0=Mi4wQUFEQU9ud2JBQUFBSUlJVWEwVGxDaVlBQUFCZ0FsVk5KdTJUV0FCUXBpM0JHZEgwdU9UUTlxNmo0emE1akJ6Sy1n|1483514867|1e9dfd28d82cefcac0dd2c382c1f32f548021c6e; __utma=155987696.1542748018.1483515579.1483515579.1483515579.1; __utmb=155987696.0.10.1483515579; __utmc=155987696; __utmz=155987696.1483515579.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
    }

    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.zhihu.com/api/v4/members/zhou-yan-64-64/followees?include=data[*].answer_count,articles_count,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset=0&limit=20', 
            headers=self.headers, 
            callback=self.index_page)



    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        print(dir(response))
        print(response.json)
        json_res = response.json
        
        if not json_res['paging']['is_end']:

            self.crawl(json_res['paging']['next'], 
                headers=self.headers,  
                callback=self.index_page)


        for item in json_res['data']:            
            self.crawl('https://www.zhihu.com/people/%s/about' % (item['url_token']), 
                headers=self.headers, 
                callback=self.detail_page)

            self.crawl("https://www.zhihu.com/api/v4/members/%s/followees?include=data[*].answer_count,articles_count,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset=0&limit=20" % (item['url_token']), 

                headers=self.headers,  
                callback=self.index_page)

            self.crawl("https://www.zhihu.com/api/v4/members/%s/followers?include=data[*].answer_count,articles_count,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset=0&limit=20" % (item['url_token']), 

                headers=self.headers,  
                callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):

        values = response.doc(".zm-profile-module-desc")
        details = range(10)
        for i in range(len(values)):
            details[i] = response.doc(values[i]).find(".ProfileItem-text").text()

        values = response.doc(".profile-navbar a")
        actions = range(10)
        for i in range(len(values)):
            actions[i] = response.doc(values[i]).find("span").text()

        values = response.doc(".zm-profile-details-reputation .zm-profile-module-desc span")
        reputations = range(10)
        for i in range(len(values)):
            reputations[i] = response.doc(values[i]).text()

        return {
            "url": response.url,
            "name": response.doc(response.doc(".title-section a")[0]).text(),
            "location": details[2],
            "education": details[3],
            "employment": details[1],
            "bio": response.doc(response.doc(".title-section div")[0]).text(),
            "content": response.doc(response.doc(".zm-profile-header-description span span.fold-item span")[0]).text(),
            "avatar": response.doc(response.doc(".zm-profile-header-main .Avatar")[0]).attr('src'),
            "ask": actions[1],
            "answer": actions[2],
            "agree": reputations[1],
            "thanks": reputations[2],
        }
    

    def on_result(self, result, task, response):
        logger.info('hello i am working')
        logger.info(result)

        sql = SQL()
        sql.replace('info',**result)