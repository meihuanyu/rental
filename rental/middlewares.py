#!/usr/bin/python
# -*-coding:utf-8-*-

import time
import random
from scrapy.downloadermiddlewares.retry import RetryMiddleware #代理ip，这是固定的导入
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import pymongo
import logging
import utils

class TimeoutIp(RetryMiddleware):
    def __init__(self,ip=''):

        '''初始化数据库'''
        connection = pymongo.MongoClient('127.0.0.1',27017)
        db = connection["ipproxy"]
        self.collection = db["iwjw"]

        '''初始化数据 '''
        self.ipnum = 0
        self.ipps=list(self.collection.find({"save_time":{"$lt":str(time.time())}}))

    def process_request(self, request, spider):
        '''轮训ip 排排坐'''
        self.ipnum +=1
        self.ipnum = self.ipnum%len(self.ipps)
        request.meta["proxy"] = '%s%s:%s' % ('http://',self.ipps[self.ipnum]['ip'],self.ipps[self.ipnum]['port'])
        #request.meta["proxy"] = "http://111.13.71.119:80"

        _iptext='%s%s' % ('切换ip:',request.meta["proxy"])
        utils.log(_iptext)
    def process_response(self, request, response, spider):
        try:
            if request.meta['download_latency']>2:

                self.errotRepeat('IpErrNum','超时ip:',10)
            else:
                self.ipps[self.ipnum]['IpErrNum'] = 0

            if response.status>400:

                self.errotRepeat('ResErrNum','请求400错误:',10)
            else:
                self.ipps[self.ipnum]['ResErrNum'] = 0

            return response
        except Exception, e:
            logging.warning(e)
            return response

    def process_exception(self, request, exception, spider):
        if "User timeout" in str(exception):
            self.errotRepeat('userTimeout', 'User timeout错误:',10)
        elif "side: 61" in str(exception):
            self.errotRepeat('sideError', 'side: 61错误:',10)
        elif "OpenSSL.SSL.Error" in  str(exception):
            self.errotRepeat('opensslError', 'openssl error:', 10)
        else:
            self.errotRepeat('accidentError', '意外的错误:', 10)
            _errtext='%s%s%s%s' % ('意外的错误',request.meta['proxy'],'--',request.url)
            logging.warning(_errtext)
            logging.warning(exception)
    '''返回ipps
    params: updateNum 更新save_time
    return 所有可用ip
    '''
    def getIppsAndUpdatetime(self,updateNum):
        if updateNum:
            self.collection.update_one({"_id": self.ipps[updateNum]['_id']},
                                       {"$set": {
                                           "save_time": str(time.time() + 86400),
                                           "areOk":0
                                       }})
            logging.warning('已废弃----ip:'+self.ipps[updateNum]['ip'])

        self.ipps = list(self.collection.find({"save_time": {"$lt": str(time.time())}}))
        return self.ipps
    def errotRepeat(self,errKey,errVal,_errnum):
        if errKey in self.ipps[self.ipnum]:
            self.ipps[self.ipnum][errKey] += 1
            _errtext = '%s%s%s%s' % (errVal, self.ipps[self.ipnum]['ip'], '次数:', self.ipps[self.ipnum][errKey])
            logging.warning(_errtext)
        else:
            self.ipps[self.ipnum][errKey] = 0

        if self.ipps[self.ipnum][errKey] == _errnum:
            logging.warning(errVal+"已达10次开始重置---")
            self.ipps = self.getIppsAndUpdatetime(self.ipnum)

    def setTime(self):
        allip=self.collection.find()
        for ip in allip:
            self.collection.update_one({"_id": ip['_id']},
                                       {"$set": {
                                           "save_time": str(time.time()),
                                           "areOk":1
                                       }})
class RotateUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        if ua:
            request.headers.setdefault('User-Agent', ua)

            # the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape

    # for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]