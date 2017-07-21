# -*- coding: utf-8 -*-
import scrapy
import json
import utils
from scrapy.http import Request
from rental.items import RentalItem
from sql import SqlManager
import logging

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class IwjwSpider(scrapy.Spider):
    name = "iwjw_data"
    allowed_domains = ["iwjw.com"]
    sql = SqlManager()

    def start_requests(self):
        subwayUrl="https://www.iwjw.com/getCitySubwayLines.action?p=2&ht=1"
        yield Request(subwayUrl, callback=self.parse, dont_filter=True)
    def parse(self, response):
        try:
            subwayConten = json.loads(response.text)['data']
            for items in subwayConten:
                for item in items['subList']:
                    _url = '%s%s' % ("https://www.iwjw.com/getMapListById.action?p=2&ht=&g=5&id=", item['id'])
                    #utils.log('login...' + _url)
                    yield Request(_url, callback=self.getMapParse, dont_filter=True)
        except:
            logging.warning('**404**'+subwayUrl+'...**')
    def getMapParse(self,response):
        try:
            getDistrict = json.loads(response.text)['data']
            for item in getDistrict['markList']:
                _url = '%s%s%s%s' % (
                "https://www.iwjw.com/getMapListById.action?g=", item['g'], '&code=', item['code'])
                #utils.log('login...'+_url)
                yield Request(_url, callback=self.getHouses, dont_filter=True)
        except :
            logging.warning('****.this subway no data..**'+response.url)

    def getHouses(self, response):
        rentalItem = RentalItem()
        get_Houses = json.loads(response.text)['data']['markList']

        for item in get_Houses:
            try:
                itemImg = []
                #地铁
                if "subWayInfoList" in item and len(item['subWayInfoList']):
                    len(item['subWayInfoList'])
                    subwayContent = sorted(item['subWayInfoList'], key=lambda _item: _item['distance'])
                    rentalItem['subway'] = unicode.encode(subwayContent[0]['subwaylineName'])
                else:
                    rentalItem['subway'] = ''
                #图片
                if 'images' in item:
                    if 'listMidImage' in item['images']:
                        for imgs in item['images']['listMidImage']:
                            itemImg.append(unicode.encode(imgs['key']))
                ##小区
                if 'houseTitle' in item:
                    rentalItem['houseTitle'] = unicode.encode(item['houseTitle'])
                else :
                    rentalItem['houseTitle'] = ''
                ##房子面积
                if 'spaceArea' in item:
                    rentalItem['housesArea'] = item['spaceArea']
                else :
                    rentalItem['housesArea'] = ''
                ##缩略图
                if 'defaultSmallPic' in item:
                    rentalItem['defaultSmallPic'] = unicode.encode(item['defaultSmallPic'])
                else:
                    rentalItem['defaultSmallPic'] = ''
                rentalItem['subwayName'] = unicode.encode(item['townName'])
                rentalItem['title'] = unicode.encode(item['estateName'])  ##标题
                rentalItem['link'] = unicode.encode(
                    '%s%s' % ("https://www.iwjw.com/", item['houseDetailUrl']))  ##链接
                rentalItem['money'] = unicode.encode(item['price'])  ##价钱
                rentalItem['address'] = unicode.encode(item['address'])  ##地址
                rentalItem['cityName'] = unicode.encode(item['cityName'])  ##房屋的配置设施
                rentalItem['bedroomSum'] = item['bedroomSum']  ##卧室
                rentalItem['livingRoomSum'] = item['livingRoomSum']  ##客厅
                rentalItem['wcSum'] = item['wcSum']  ##厕所

                rentalItem['listMidImage'] = itemImg
                self.sql.insert_data(self.name, rentalItem)
                utils.log(json.dumps(rentalItem._values))
            except Exception, e:
                logging.warning(e)
                logging.warning("错误!!!!" + response.url)