# -*- coding: utf-8 -*-
import re
import time
# 反爬虫经验：一被封禁就先换user-agent再更新cookies，因为一被封禁cookies很大概率会变
import scrapy
import random
from rentSpider.items import RentspiderItem

class BjHouseSpider(scrapy.Spider):
    name = 'bj_house'
    allowed_domains = ['bj.lianjia.com']
    start_urls = ['https://bj.lianjia.com/zufang/']

    # 将 Cookie 复制到变量中
    cookies = {
        'lianjia_uuid': 'dcb04c88-68ce-4a4e-8b5f-d7f95d4042b3',
        '_ga': 'GA1.2.1357761050.1734095280',
        'crosSdkDT2019DeviceId': '-1zlpha-8pbec2-ez5djc31jblzojd-wbn4kxoo4',
        'lfrc_': '5e1c63c9-3224-443a-9a9f-ce58fe21c13f',
        '_jzqa': '1.2078144481677403400.1734172811.1734172811.1734172811.1',
        '_qzja': '1.389294859.1734172810750.1734172810750.1734172810750.1734172810750.1734172810750.0.0.0.1.1',
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22193c4c11f301476-06db7e551211e5-4c657b58-1327104-193c4c11f31aa8%22%2C%22%24device_id%22%3A%22193c4c11f301476-06db7e551211e5-4c657b58-1327104-193c4c11f31aa8%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D',
        'Hm_lvt_46bf127ac9b856df503ec2dbf942b67e': '1734095279,1734141502,1734229669',
        '_ga_RCTBRFLNVS': 'GS1.2.1734229669.6.1.1734229674.0.0.0',
        'ftkrc_': 'ef0394c8-a411-4dc5-8ea4-8657779b9107',
        'login_ucid': '2000000455305450',
        'lianjia_token': '2.0012f8e95b455eec5d0355c06a31b36af0',
        'lianjia_token_secure': '2.0012f8e95b455eec5d0355c06a31b36af0',
        'security_ticket': 'PU04GzoyhxbO5oAdgX90mGiQhuXC/kTTm2peO+hwtODp5lR4pAmf8RE8XE/XBvMcp3gVTeAxdEv4Xno8e1pw6pEvEVkAKmpXV039Dlr8OuNaqtsxaoP+fvcJGAie7sC7Gfn/KGFXLFQFyQhPuJcHsxronfOjTJxZSSCkIkg82yM=',
        'GUARANTEE_POPUP_SHOW': 'true',
        'GUARANTEE_BANNER_SHOW': 'true',
        'lianjia_ssid': 'a57160f5-3e73-4c12-99e0-94e7233d515e',
        'select_city': '110000',
        'srcid': 'eyJ0Ijoie1wiZGF0YVwiOlwiNjFjNTM5MTc4ZGMwMjM4NjZlNjVlMzg0MTE0MWI0ZjQxMGRhMjdlNDMzNWQ5MzJlMTE1NmIyNWRmYmNiNTE3ZDUxNzhmOTA1NDhmNmEyMjg4YzA1YTQ4ZTZkNWM4ZGMzZGFlYTE5ZWVhNWQyZWJhYzNlMzkxZWM3ZjYzNTk5ZDRhMGQ0YzM5YmNhYmZkM2QyYmFhYzZkZmMyYzJmZjZkOWFhMTZmZjMwNTdmY2JjY2JlZjBkMmQyYzEyNjZkZDBjN2RlMDVhYjQ1YjBmNjBkZGQwZmNlYmZmOTU1NzY2YWVmYmVkNDM2ODdlNTYyYjk0Y2Q1MGM5YWM4NTdlYzAzY1wiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJkNjU0NWI5Y1wifSIsInIiOiJodHRwczovL2JqLmxpYW5qaWEuY29tL3p1ZmFuZy8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==',
    }

    def parse(self, response):
        for url in response.xpath('//*[@id="filter"]/ul[2]/li/a/@href').extract()[1:]:
            yield scrapy.Request(
                url='https://bj.lianjia.com/' + url,
                callback=self.page,
                cookies=self.cookies  # 添加 Cookie
            )

    def page(self, response):
        delay = random.uniform(5, 6)
        time.sleep(delay)
        page = response.xpath('//*[@id="content"]/div[1]/div[2]/@data-totalpage').extract()
        if not page:
            page = 2
        else:
            page = eval(page[0]) + 1
        for i in range(1, page):
            yield scrapy.Request(
                url=response.url + 'pg{}'.format(i),
                callback=self.detail,
                headers=self.cookies  # 添加 Cookie
            )

    def detail(self, response):
        for div in response.xpath('//div[@class="content__list--item" and @data-ad_code!="1"]'):
            item = RentspiderItem()

            # 提取标题（title）
            title = div.xpath(
                './div[@class="content__list--item--main"]/p[@class="content__list--item--title"]/a/text()').extract_first()
            item['title'] = title.strip() if title else "未知标题"

            # 提取地区（district）
            district = div.xpath(
                './div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/a[2]/text()').extract_first()
            item['district'] = district.strip() if district else "未知地区"

            # 提取并清洗面积、朝向、户型相关信息
            raw_text = div.xpath(
                './div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/text()').extract()
            cleaned_text = [text.strip() for text in raw_text if text.strip() and text.strip() != '-']
            #print(f"Cleaned Text: {cleaned_text}")  # 调试打印清洗后的文本

            # 提取面积（area）
            area_text = next((text for text in cleaned_text if '㎡' in text), None)
            item['area'] = float(area_text.replace('㎡', '').strip()) if area_text else 0.0

            # 提取朝向（direction）
            direction_text = next((text for text in cleaned_text if any(d in text for d in ['东', '西', '南', '北'])),
                                  None)
            item['direction'] = direction_text if direction_text else "未知朝向"

            # 提取户型（types）
            types_text = next((text for text in cleaned_text if '室' in text), None)
            item['types'] = types_text.strip() if types_text else "3室2厅1卫"

            # 提取价格（price）
            price = div.xpath(
                './div[@class="content__list--item--main"]/span[@class="content__list--item-price"]/em/text()').extract_first()
            try:
                item['price'] = int(price.strip()) if price else 0
            except ValueError:
                item['price'] = 0

            # 返回解析的 item
            yield item

class ShHouseSpider(scrapy.Spider):
    name = 'sh_house'
    allowed_domains = ['sh.lianjia.com']
    start_urls = ['https://sh.lianjia.com/zufang/']

    # 将 Cookie 复制到变量中
    cookies = {
        'lianjia_uuid': 'dcb04c88-68ce-4a4e-8b5f-d7f95d4042b3',
        '_ga': 'GA1.2.1357761050.1734095280',
        'crosSdkDT2019DeviceId': '-1zlpha-8pbec2-ez5djc31jblzojd-wbn4kxoo4',
        'lfrc_': '5e1c63c9-3224-443a-9a9f-ce58fe21c13f',
        '_jzqa': '1.2078144481677403400.1734172811.1734172811.1734172811.1',
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22193c4c11f301476-06db7e551211e5-4c657b58-1327104-193c4c11f31aa8%22%2C%22%24device_id%22%3A%22193c4c11f301476-06db7e551211e5-4c657b58-1327104-193c4c11f31aa8%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D',
        'Hm_lvt_46bf127ac9b856df503ec2dbf942b67e': '1734095279,1734141502,1734229669',
        '_ga_RCTBRFLNVS': 'GS1.2.1734229669.6.1.1734229674.0.0.0',
        'ftkrc_': 'ef0394c8-a411-4dc5-8ea4-8657779b9107',
        'login_ucid': '2000000455305450',
        'lianjia_token': '2.0012f8e95b455eec5d0355c06a31b36af0',
        'lianjia_token_secure': '2.0012f8e95b455eec5d0355c06a31b36af0',
        'security_ticket': 'PU04GzoyhxbO5oAdgX90mGiQhuXC/kTTm2peO+hwtODp5lR4pAmf8RE8XE/XBvMcp3gVTeAxdEv4Xno8e1pw6pEvEVkAKmpXV039Dlr8OuNaqtsxaoP+fvcJGAie7sC7Gfn/KGFXLFQFyQhPuJcHsxronfOjTJxZSSCkIkg82yM=',
        'GUARANTEE_POPUP_SHOW': 'true',
        'GUARANTEE_BANNER_SHOW': 'true',
        'lianjia_ssid': 'bc877e07-1bac-4515-b7e9-8493d8815fa4',
        'select_city': '310000',
        'srcid': 'eyJ0Ijoie1wiZGF0YVwiOlwiNjFjNTM5MTc4ZGMwMjM4NjZlNjVlMzg0MTE0MWI0ZjQxMGRhMjdlNDMzNWQ5MzJlMTE1NmIyNWRmYmNiNTE3ZDUxNzhmOTA1NDhmNmEyMjg4YzA1YTQ4ZTZkNWM4ZGMzZGFlYTE5ZWVhNWQyZWJhYzNlMzkxZWM3ZjYzNTk5ZDRhMGQ0YzM5YmNhYmZkM2QyYmFhYzZkZmMyYzJmZjZkOWZjZmYzZDQ3YzAyOWY4ZmM5Y2VhMmFkZDUxYWIyNTlkY2JiN2ZiN2YzMjIyNzUxN2U5MWY5NmRkOWY4MDdmOTZjMzUyZTgwNTQyMGQyYzg5ZTI4Y2E2MGE3MjgxYTUxM1wiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI3Y2EzYjk4MlwifSIsInIiOiJodHRwczovL3NoLmxpYW5qaWEuY29tL3p1ZmFuZy8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ=='
    }

    def parse(self, response):
        for url in response.xpath('//*[@id="filter"]/ul[2]/li/a/@href').extract()[1:]:
            yield scrapy.Request(
                url='https://sh.lianjia.com/' + url,
                callback=self.page,
                cookies=self.cookies  # 添加 Cookie
            )

    def page(self, response):
        delay = random.uniform(5, 6)
        time.sleep(delay)
        page = response.xpath('//*[@id="content"]/div[1]/div[2]/@data-totalpage').extract()
        if not page:
            page = 2
        else:
            page = eval(page[0]) + 1
        for i in range(1, page):
            yield scrapy.Request(
                url=response.url + 'pg{}'.format(i),
                callback=self.detail,
                cookies=self.cookies  # 添加 Cookie
            )

    def detail(self, response):
        for div in response.xpath('//div[@class="content__list--item" and @data-ad_code!="1"]'):
            item = RentspiderItem()

            # 提取标题（title）
            title = div.xpath(
                './div[@class="content__list--item--main"]/p[@class="content__list--item--title"]/a/text()').extract_first()
            item['title'] = title.strip() if title else "未知标题"

            # 提取地区（district）
            district = div.xpath(
                './div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/a[2]/text()').extract_first()
            item['district'] = district.strip() if district else "未知地区"

            # 提取并清洗面积、朝向、户型相关信息
            raw_text = div.xpath(
                './div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/text()').extract()
            cleaned_text = [text.strip() for text in raw_text if text.strip() and text.strip() != '-']
            print(f"Cleaned Text: {cleaned_text}")  # 调试打印清洗后的文本

            # 提取面积（area）
            area_text = next((text for text in cleaned_text if '㎡' in text), None)
            item['area'] = float(area_text.replace('㎡', '').strip()) if area_text else 0.0

            # 提取朝向（direction）
            direction_text = next((text for text in cleaned_text if any(d in text for d in ['东', '西', '南', '北'])),
                                  None)
            item['direction'] = direction_text if direction_text else "未知朝向"

            # 提取户型（types）
            types_text = next((text for text in cleaned_text if '室' in text), None)
            item['types'] = types_text.strip() if types_text else "3室2厅1卫"

            # 提取价格（price）
            price = div.xpath(
                './div[@class="content__list--item--main"]/span[@class="content__list--item-price"]/em/text()').extract_first()
            try:
                item['price'] = int(price.strip()) if price else 0
            except ValueError:
                item['price'] = 0

            # 返回解析的 item
            yield item

class GzHouseSpider(scrapy.Spider):
    name = 'gz_house'
    allowed_domains = ['gz.lianjia.com']
    start_urls = ['https://gz.lianjia.com/zufang/']

    # 将 Cookie 复制到变量中
    cookies = {
        'lianjia_uuid': 'dcb04c88-68ce-4a4e-8b5f-d7f95d4042b3',
        '_ga': 'GA1.2.1357761050.1734095280',
        'crosSdkDT2019DeviceId': '-1zlpha-8pbec2-ez5djc31jblzojd-wbn4kxoo4',
        'lfrc_': '5e1c63c9-3224-443a-9a9f-ce58fe21c13f',
        '_jzqa': '1.2078144481677403400.1734172811.1734172811.1734172811.1',
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22193c4c11f301476-06db7e551211e5-4c657b58-1327104-193c4c11f31aa8%22%2C%22%24device_id%22%3A%22193c4c11f301476-06db7e551211e5-4c657b58-1327104-193c4c11f31aa8%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D',
        'Hm_lvt_46bf127ac9b856df503ec2dbf942b67e': '1734095279,1734141502,1734229669',
        '_ga_RCTBRFLNVS': 'GS1.2.1734229669.6.1.1734229674.0.0.0',
        'ftkrc_': 'ef0394c8-a411-4dc5-8ea4-8657779b9107',
        'login_ucid': '2000000455305450',
        'lianjia_token': '2.0012f8e95b455eec5d0355c06a31b36af0',
        'lianjia_token_secure': '2.0012f8e95b455eec5d0355c06a31b36af0',
        'security_ticket': 'PU04GzoyhxbO5oAdgX90mGiQhuXC/kTTm2peO+hwtODp5lR4pAmf8RE8XE/XBvMcp3gVTeAxdEv4Xno8e1pw6pEvEVkAKmpXV039Dlr8OuNaqtsxaoP+fvcJGAie7sC7Gfn/KGFXLFQFyQhPuJcHsxronfOjTJxZSSCkIkg82yM=',
        'lianjia_ssid': 'bc877e07-1bac-4515-b7e9-8493d8815fa4',
        'select_city': '440100',
        'GUARANTEE_POPUP_SHOW': 'true',
        'hip': '4NUzcKApV6bRgkW2OdRTNMo5A9MjyMdi0YiRXReuO292AoOfLZPjLRDmPHIzcs7Gxtn5MXkRPQpRWlcK5WRYkpzZFyZo0Hui3DWn9CrzIz2ikoszIzLZz7ATN-qEhSMCqbJJah8UA8y-fMzEqMGyorf4arvpXRzW0855irwCijh7AvxkZNmhBJelRQ%3D%3D',
        'srcid': 'eyJ0Ijoie1wiZGF0YVwiOlwiNjFjNTM5MTc4ZGMwMjM4NjZlNjVlMzg0MTE0MWI0ZjQxMGRhMjdlNDMzNWQ5MzJlMTE1NmIyNWRmYmNiNTE3ZDUxNzhmOTA1NDhmNmEyMjg4YzA1YTQ4ZTZkNWM4ZGMzZGFlYTE5ZWVhNWQyZWJhYzNlMzkxZWM3ZjYzNTk5ZDRhMGQ0YzM5YmNhYmZkM2QyYmFhYzZkZmMyYzJmZjZkOTJkOTQ3Y2ZlNjM0NmU2OWViN2IxOGY2Y2Y2ZmUwNjUwOTQ4M2RlMjI5OWE2MGFlNGQzMzdlODY2NGRmMWU5ZTAyYjJmMDAyNTQ0NDhhYTA3OTM3MjdmMTE2YjE0MjhhNlwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJ4YzM5YTllMlwiLFwiZGV0YWFpZXwiOlwiYmQ1NzU2YjMiLCJzY2hlbWVfY2lkXCI6XCJ0ZDFmZTM2NDAwM2I1ZTlkNzM4ZWZmNzJlODk1ZTY0YzI5YmYzZWFjM2FkXCI9'
    }

    def parse(self, response):
        for url in response.xpath('//*[@id="filter"]/ul[2]/li/a/@href').extract()[1:]:
            yield scrapy.Request(
                url='https://gz.lianjia.com/' + url,
                callback=self.page,
                cookies=self.cookies  # 添加 Cookie
            )

    def page(self, response):
        delay = random.uniform(5, 6)
        time.sleep(delay)
        page = response.xpath('//*[@id="content"]/div[1]/div[2]/@data-totalpage').extract()
        if not page:
            page = 2
        else:
            page = eval(page[0]) + 1
        for i in range(1, page):
            yield scrapy.Request(
                url=response.url + 'pg{}'.format(i),
                callback=self.detail,
                cookies=self.cookies  # 添加 Cookie
            )

    def detail(self, response):
        for div in response.xpath('//div[@class="content__list--item" and @data-ad_code!="1"]'):
            item = RentspiderItem()

            # 提取标题（title）
            title = div.xpath(
                './div[@class="content__list--item--main"]/p[@class="content__list--item--title"]/a/text()').extract_first()
            item['title'] = title.strip() if title else "未知标题"

            # 提取地区（district）
            district = div.xpath(
                './div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/a[2]/text()').extract_first()
            item['district'] = district.strip() if district else "未知地区"

            # 提取并清洗面积、朝向、户型相关信息
            raw_text = div.xpath(
                './div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/text()').extract()
            cleaned_text = [text.strip() for text in raw_text if text.strip() and text.strip() != '-']
            print(f"Cleaned Text: {cleaned_text}")  # 调试打印清洗后的文本

            # 提取面积（area）
            area_text = next((text for text in cleaned_text if '㎡' in text), None)
            item['area'] = float(area_text.replace('㎡', '').strip()) if area_text else 0.0

            # 提取朝向（direction）
            direction_text = next((text for text in cleaned_text if any(d in text for d in ['东', '西', '南', '北'])),
                                  None)
            item['direction'] = direction_text if direction_text else "未知朝向"

            # 提取户型（types）
            types_text = next((text for text in cleaned_text if '室' in text), None)
            item['types'] = types_text.strip() if types_text else "3室2厅1卫"

            # 提取价格（price）
            price = div.xpath(
                './div[@class="content__list--item--main"]/span[@class="content__list--item-price"]/em/text()').extract_first()
            try:
                item['price'] = int(price.strip()) if price else 0
            except ValueError:
                item['price'] = 0

            # 返回解析的 item
            yield item

class SzHouseSpider(scrapy.Spider):
    name = 'sz_house'
    allowed_domains = ['sz.lianjia.com']
    start_urls = ['https://sz.lianjia.com/zufang/']

    # 将 Cookie 复制到变量中
    cookies = {
        'lianjia_uuid': 'dcb04c88-68ce-4a4e-8b5f-d7f95d4042b3',
        '_ga': 'GA1.2.1357761050.1734095280',
        'crosSdkDT2019DeviceId': '-1zlpha-8pbec2-ez5djc31jblzojd-wbn4kxoo4',
        'lfrc_': '5e1c63c9-3224-443a-9a9f-ce58fe21c13f',
        '_jzqa': '1.2078144481677403400.1734172811.1734172811.1734172811.1',
        'sensorsdata2015jssdkcross': '{"distinct_id":"193c4c11f301476-06db7e551211e5-4c657b58-1327104-193c4c11f31aa8","$device_id":"193c4c11f301476-06db7e551211e5-4c657b58-1327104-193c4c11f31aa8","props":{"$latest_traffic_source_type":"直接流量","$latest_referrer":"","$latest_referrer_host":"","$latest_search_keyword":"未取得值_直接打开"}}',
        'Hm_lvt_46bf127ac9b856df503ec2dbf942b67e': '1734095279,1734141502,1734229669',
        '_ga_RCTBRFLNVS': 'GS1.2.1734229669.6.1.1734229674.0.0.0',
        'ftkrc_': 'ef0394c8-a411-4dc5-8ea4-8657779b9107',
        'login_ucid': '2000000455305450',
        'lianjia_token': '2.0012f8e95b455eec5d0355c06a31b36af0',
        'lianjia_token_secure': '2.0012f8e95b455eec5d0355c06a31b36af0',
        'security_ticket': 'PU04GzoyhxbO5oAdgX90mGiQhuXC/kTTm2peO+hwtODp5lR4pAmf8RE8XE/XBvMcp3gVTeAxdEv4Xno8e1pw6pEvEVkAKmpXV039Dlr8OuNaqtsxaoP+fvcJGAie7sC7Gfn/KGFXLFQFyQhPuJcHsxronfOjTJxZSSCkIkg82yM=',
        'lianjia_ssid': 'bc877e07-1bac-4515-b7e9-8493d8815fa4',
        'select_city': '440300',
        'GUARANTEE_POPUP_SHOW': 'true',
        'GUARANTEE_BANNER_SHOW': 'true',
        'hip': '2O4CrED0ilfFj5c0Cj0cGmK8t49Py9bpyuKHry_s895-szLmU6psqEDI_YRuFH7LhS6OPc8R8SjIfeb44tCl71G47YfHtHuiqgYgVKWBFKhrWuDEUMzizCUAjZybVgy8zeQ-OyeXEN5v_9OdipaILaTB0h9lntjzdQIAk2ah2n45A0AeuCQ0qB0xFQ==',
        'srcid': 'eyJ0Ijoie1wiZGF0YVwiOlwiNjFjNTM5MTc4ZGMwMjM4NjZlNjVlMzg0MTE0MWI0ZjQxMGRhMjdlNDMzNWQ5MzJlMTE1NmIyNWRmYmNiNTE3ZDUxNzhmOTA1NDhmNmEyMjg4YzA1YTQ4ZTZkNWM4ZGMzZGFlYTE5ZWVhNWQyZWJhYzNlMzkxZWM3ZjYzNTk5ZDRhMGQ0YzM5YmNhYmZkM2QyYmFhYzZkZmMyYzJmZjZkOWFiYTE5ZTc0MmJhZGQwYWZjNGMzMDRiZWNmODcwNDY3NzMxNmJiY2QxZmZlMGZiZWJlMGMwNjIyNjgzNTYxYmZkYjA5YzAxZTE4YjY2ZTM0YTM3NGFiYjU1YzkyMGZjZVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI1NjMzM2I3NlwifSIsInIiOiJodHRwczovL3N6LmxpYW5qaWEuY29tL3p1ZmFuZyIsIm9zIjoid2ViIiwidiI6IjAuMSJ9'
    }

    def parse(self, response):
        for url in response.xpath('//*[@id="filter"]/ul[2]/li/a/@href').extract()[1:]:
            yield scrapy.Request(
                url='https://sz.lianjia.com/' + url,
                callback=self.page,
                cookies=self.cookies  # 添加 Cookie
            )

    def page(self, response):
        delay = random.uniform(5, 6)
        time.sleep(delay)
        page = response.xpath('//*[@id="content"]/div[1]/div[2]/@data-totalpage').extract()
        if not page:
            page = 2
        else:
            page = eval(page[0]) + 1
        for i in range(1, page):
            yield scrapy.Request(
                url=response.url + 'pg{}'.format(i),
                callback=self.detail,
                cookies=self.cookies  # 添加 Cookie
            )

    def detail(self, response):
        for div in response.xpath('//div[@class="content__list--item" and @data-ad_code!="1"]'):
            item = RentspiderItem()

            # 提取标题（title）
            title = div.xpath(
                './div[@class="content__list--item--main"]/p[@class="content__list--item--title"]/a/text()').extract_first()
            item['title'] = title.strip() if title else "未知标题"

            # 提取地区（district）
            district = div.xpath(
                './div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/a[2]/text()').extract_first()
            item['district'] = district.strip() if district else "未知地区"

            # 提取并清洗面积、朝向、户型相关信息
            raw_text = div.xpath(
                './div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/text()').extract()
            cleaned_text = [text.strip() for text in raw_text if text.strip() and text.strip() != '-']
            print(f"Cleaned Text: {cleaned_text}")  # 调试打印清洗后的文本

            # 提取面积（area）
            area_text = next((text for text in cleaned_text if '㎡' in text), None)
            item['area'] = float(area_text.replace('㎡', '').strip()) if area_text else 0.0

            # 提取朝向（direction）
            direction_text = next((text for text in cleaned_text if any(d in text for d in ['东', '西', '南', '北'])),
                                  None)
            item['direction'] = direction_text if direction_text else "未知朝向"

            # 提取户型（types）
            types_text = next((text for text in cleaned_text if '室' in text), None)
            item['types'] = types_text.strip() if types_text else "3室2厅1卫"

            # 提取价格（price）
            price = div.xpath(
                './div[@class="content__list--item--main"]/span[@class="content__list--item-price"]/em/text()').extract_first()
            try:
                item['price'] = int(price.strip()) if price else 0
            except ValueError:
                item['price'] = 0

            # 返回解析的 item
            yield item

class ZzHouseSpider(scrapy.Spider):
    name = 'zz_house'
    allowed_domains = ['zz.lianjia.com']
    start_urls = ['https://zz.lianjia.com/zufang/']

    # 将 Cookie 复制到变量中
    cookies = {
        'lianjia_uuid': 'dcb04c88-68ce-4a4e-8b5f-d7f95d4042b3',
        '_ga': 'GA1.2.1357761050.1734095280',
        'crosSdkDT2019DeviceId': '-1zlpha-8pbec2-ez5djc31jblzojd-wbn4kxoo4',
        'lfrc_': '5e1c63c9-3224-443a-9a9f-ce58fe21c13f',
        '_jzqa': '1.2078144481677403400.1734172811.1734172811.1734172811.1',
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22193c4c11f301476-06db7e551211e5-4c657b58-1327104-193c4c11f31aa8%22%2C%22%24device_id%22%3A%22193c4c11f301476-06db7e551211e5-4c657b58-1327104-193c4c11f31aa8%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D',
        'Hm_lvt_46bf127ac9b856df503ec2dbf942b67e': '1734095279,1734141502,1734229669',
        '_ga_RCTBRFLNVS': 'GS1.2.1734229669.6.1.1734229674.0.0.0',
        'ftkrc_': 'ef0394c8-a411-4dc5-8ea4-8657779b9107',
        'login_ucid': '2000000455305450',
        'lianjia_token': '2.0012f8e95b455eec5d0355c06a31b36af0',
        'lianjia_token_secure': '2.0012f8e95b455eec5d0355c06a31b36af0',
        'security_ticket': 'PU04GzoyhxbO5oAdgX90mGiQhuXC/kTTm2peO+hwtODp5lR4pAmf8RE8XE/XBvMcp3gVTeAxdEv4Xno8e1pw6pEvEVkAKmpXV039Dlr8OuNaqtsxaoP+fvcJGAie7sC7Gfn/KGFXLFQFyQhPuJcHsxronfOjTJxZSSCkIkg82yM=',
        'GUARANTEE_POPUP_SHOW': 'true',
        'lianjia_ssid': '1a8ce123-21dc-4a72-8cb4-cc2c2d27c72a',
        'select_city': '410100',
        'hip': 'NvYZYbY9Vb_pJsta0fZsPh5-8QvCCQWd-0RJSasRAoNww51aQt2QXplGSIqEUq8rW5hTmXYgsJWWznjY7jfw0hz5dAvP8oSssheR4dSDSGg3l72u7qztvT5BAcvdbL9l1lISXkSQZmJih5wVNA0kYCeqZ27dix8vJ9O3QnKrdPgXYX5f05K_quwi0w%3D%3D',
        'srcid': 'eyJ0Ijoie1wiZGF0YVwiOlwiNTE4NGJkOGYyZGM1MjI1ZjFhYmE2MmQ4YTQyOGEwZTQ0MjkzOWMxMGE4MjdmYjIyY2M0ZjE5OGFjY2I5YTA5NDRiM2MyZWE4NzVhZjNkMmI0NWI3NDliMWFmMzJlYzQyMjFkYjUzNDBmNzU0Y2I1YTYxZWM0NWZhOGVlMDEzZDIzMTNlY2U5MzFiMTIxNmY0YmU5MWI3ZDBjNmY4YTZiM2VhYThiNWFjYTA4ZGE4ZTE1NGNiYzgwMGM5OGQ1NjhiZjkwNzdiMDUyMjNkYWQzZTA5OGYzNDZkZGM2MWU3YzNmM2M1YjI4MTdmNzU1ZGZlYWVhNWU3N2E0NmE3MzliMFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCIyOTIzMzMxY1wifSIsInIiOiJodHRwczovL3p6LmxpYW5qaWEuY29tL3p1ZmFuZy8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==',
    }

    def parse(self, response):
        for url in response.xpath('//*[@id="filter"]/ul[2]/li/a/@href').extract()[1:]:
            yield scrapy.Request(
                url='https://zz.lianjia.com/' + url,
                callback=self.page,
                cookies=self.cookies  # 添加 Cookie
            )

    def page(self, response):
        delay = random.uniform(5, 6)
        time.sleep(delay)
        page = response.xpath('//*[@id="content"]/div[1]/div[2]/@data-totalpage').extract()
        if not page:
            page = 2
        else:
            page = eval(page[0]) + 1
        for i in range(1, page):
            yield scrapy.Request(
                url=response.url + 'pg{}'.format(i),
                callback=self.detail,
                cookies=self.cookies  # 添加 Cookie
            )

    def detail(self, response):
        for div in response.xpath('//div[@class="content__list--item" and @data-ad_code!="1"]'):
            item = RentspiderItem()

            # 提取标题（title）
            title = div.xpath(
                './div[@class="content__list--item--main"]/p[@class="content__list--item--title"]/a/text()').extract_first()
            item['title'] = title.strip() if title else "未知标题"

            # 提取地区（district）
            district = div.xpath(
                './div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/a[2]/text()').extract_first()
            item['district'] = district.strip() if district else "未知地区"

            # 提取并清洗面积、朝向、户型相关信息
            raw_text = div.xpath(
                './div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/text()').extract()
            cleaned_text = [text.strip() for text in raw_text if text.strip() and text.strip() != '-']
            print(f"Cleaned Text: {cleaned_text}")  # 调试打印清洗后的文本

            # 提取面积（area）
            area_text = next((text for text in cleaned_text if '㎡' in text), None)
            item['area'] = float(area_text.replace('㎡', '').strip()) if area_text else 0.0

            # 提取朝向（direction）
            direction_text = next((text for text in cleaned_text if any(d in text for d in ['东', '西', '南', '北'])),
                                  None)
            item['direction'] = direction_text if direction_text else "未知朝向"

            # 提取户型（types）
            types_text = next((text for text in cleaned_text if '室' in text), None)
            item['types'] = types_text.strip() if types_text else "3室2厅1卫"

            # 提取价格（price）
            price = div.xpath(
                './div[@class="content__list--item--main"]/span[@class="content__list--item-price"]/em/text()').extract_first()
            try:
                item['price'] = int(price.strip()) if price else 0
            except ValueError:
                item['price'] = 0

            # 返回解析的 item
            yield item




