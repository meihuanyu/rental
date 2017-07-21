# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RentalItem(scrapy.Item):
    title       = scrapy.Field()##标题
    link        = scrapy.Field()##链接
    money       = scrapy.Field()##价钱
    housesArea  = scrapy.Field()##房子面积
    houseTitle  = scrapy.Field()##小区
    address     = scrapy.Field()##地址
    cityName    = scrapy.Field()##房屋的配置设施
    subway      = scrapy.Field()##地铁线路
    subwayName  = scrapy.Field()##地铁站名称
    bedroomSum  = scrapy.Field()##卧室
    livingRoomSum=scrapy.Field()##客厅
    wcSum       = scrapy.Field()##厕所
    defaultSmallPic=scrapy.Field()##缩略图
    listMidImage   =scrapy.Field()##图片