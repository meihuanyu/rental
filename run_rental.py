# -*- coding: utf-8 -*-

import logging
import os
import sys
import scrapydo
import time
import utils
from rental.spiders.iwjw_spider import IwjwSpider
import rental.settings
scrapydo.setup()

spiders = [
    IwjwSpider
]

utils.log('*******************run spider start...*******************')
##增加状态码捕捉
_HTTPERROR_ALLOWED_CODES = [403, 404]

_DOWNLOAD_DELAY = 0.3

_DOWNLOAD_TIMEOUT=20

_COOKIES_ENABLED = False

_DOWNLOADER_MIDDLEWARES = {
    'rental.pipelines.RentalPipeline': 300,
}
_DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 325,
    'rental.middlewares.TimeoutIp': 326,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'rental.middlewares.RotateUserAgentMiddleware': 400,
}
_settings = {"DOWNLOADER_MIDDLEWARES": _DOWNLOADER_MIDDLEWARES, "DOWNLOADER_MIDDLEWARES": _DOWNLOADER_MIDDLEWARES,
             "HTTPERROR_ALLOWED_CODES": _HTTPERROR_ALLOWED_CODES, "COOKIES_ENABLED": _COOKIES_ENABLED,
             "DOWNLOAD_TIMEOUT":_DOWNLOAD_TIMEOUT}
for spider in spiders:
    scrapydo.run_spider(spider_cls=spider, settings=_settings)

utils.log('*******************run spider waiting...*******************')
##此处用 while 可以设置循环
#time.sleep(1200)

if __name__ == '__main__':
    os.chdir(sys.path[0])

    if not os.path.exists('log'):
        os.makedirs('log')

    logging.basicConfig(
        filename = 'log/validator.log',
        format = '%(asctime)s: %(message)s',
        level = logging.DEBUG
    )
