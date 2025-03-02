
import os
import sys
import django

BOT_NAME = 'rentSpider'

SPIDER_MODULES = ['rentSpider.spiders']
NEWSPIDER_MODULE = 'rentSpider.spiders'

#COOKIES_ENABLED = False

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edge/116.0.0.0'


# settings.py 中增加
RETRY_ENABLED = True
RETRY_TIMES = 3  # 设置重试次数

DOWNLOAD_DELAY = 2  # 设置请求延时，避免过于频繁的请求
AUTOTHROTTLE_ENABLED = True  # 启用自动调节下载速度
AUTOTHROTTLE_START_DELAY = 2  # 初始请求延时
AUTOTHROTTLE_MAX_DELAY = 10

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
   'rentSpider.pipelines.RentspiderPipeline': 300,  # Pipeline receives content
}

