# -*- coding: utf-8 -*-


BOT_NAME = 'rental'

SPIDER_MODULES = ['rental.spiders']
NEWSPIDER_MODULE = 'rental.spiders'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False
##增加状态码捕捉
HTTPERROR_ALLOWED_CODES=[403,404]

##全局设置请求失败状态
CHANGE_PROXY=False


COOKIES_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware':323,
     'rental.middlewares.IPPOOLS':324,
     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,
     'rental.middlewares.RotateUserAgentMiddleware':400,
}

ITEM_PIPELINES = {
   'rental.pipelines.RentalPipeline': 300,
}
MONGODB_SERVER='localhost'
MONGODB_PORT=27017
MONGODB_DB='reting'
MONGODB_COLLECTION='iwjw'