# -*- coding: utf-8 -*-

import logging
import pymongo
import config
import json
import time
import datetime
import utils

from proxy import Proxy
from sql_base import SqlBase


class Mongodb(SqlBase):
    def __init__(self, **kwargs):
        super(Mongodb, self).__init__(**kwargs)
        self.client = pymongo.MongoClient(**kwargs)
        self.db = self.client[config.database]

    def init_database(self, database_name):
        pass

    def init_proxy_table(self, table_name):
        pass

    def insert_proxy(self, table_name, proxy):
        data = proxy.get_dict()
        data['save_time'] = str(time.time())
        data['create_time'] = str(datetime.datetime.now())
        self.db[table_name].create_index([("ip", pymongo.DESCENDING)], unique=True)
        try:
            self.db[table_name].insert(data)
        except BaseException,e:
            if "E11000 duplicate key error collection" in e.message:
                utils.log(str(e.message.split(' ')[12])+"在数据库中从重复")
    def insert_data(self,table_name,item):
        try:
            self.db[table_name].insert(dict(item))
        except:
            pass
    def select_proxy(self, table_name, **kwargs):
        filter = {}
        if kwargs.get('anonymity') != '':
            filter['anonymity'] = kwargs.get('anonymity')
        if kwargs.get('https') != '':
            filter['https'] = kwargs.get('https')

        data = [item for item in self.db[table_name].find(filter).limit(int(kwargs.get('count')))]
        return data

    def update_proxy(self, table_name, proxy):
        self.db[table_name].update_one(
            {'_id': proxy.id},
            {'$set':
                 {'https': proxy.https, 'speed': proxy.speed, 'vali_count': proxy.vali_count,
                  'anonymity': proxy.anonymity, 'save_time': str(time.time())}})

    def delete_proxy(self, table_name, proxy):
        return self.del_proxy_with_id(table_name, proxy.id)

    def delete_old(self, table_name, day):
        start = datetime.datetime.now()
        end = datetime.datetime.now()
        pass

    def get_proxy_count(self, table_name):
        count = self.db[table_name].find().count()
        logging.debug('count:%s' % count)
        return count

    def get_proxy_ids(self, table_name):
        ids = self.db[table_name].distinct('_id')
        logging.debug('ids:%s' % ids)
        return ids

    def get_proxy_with_id(self, table_name, id):
        data = self.db[table_name].find_one({'_id': id})
        logging.debug(data)
        proxy = Proxy()
        proxy.set_value(
            ip=data.get('ip'),
            port=data.get('port'),
            country=data.get('country'),
            anonymity=data.get('country'),
            https=data.get('https'),
            speed=data.get('speed'),
            source=data.get('source'),
            vali_count=data.get('vali_count')
        )
        proxy.id = data.get('_id')
        return proxy

    def del_proxy_with_id(self, table_name, id):
        self.db[table_name].delete_one({'_id': id})
        return True

    def del_proxy_with_ip(self, table_name, ip):
        self.db[table_name].delete_one({'ip': ip})
        return True

    def commit(self):
        pass
