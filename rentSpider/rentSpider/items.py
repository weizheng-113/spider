# -*- coding: utf-8 -*-

import scrapy

class RentspiderItem(scrapy.Item):
    # 定义每个字段，并设置其数据类型（默认为Scrapy.Field()）
    title = scrapy.Field()       # 标题
    district = scrapy.Field()    # 区域
    area = scrapy.Field()        # 面积
    direction = scrapy.Field()   # 朝向
    price = scrapy.Field()       # 租金价格
    types = scrapy.Field()       # 类型（如：一居室、两居室等）