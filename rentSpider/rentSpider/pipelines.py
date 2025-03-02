import csv
import os


class RentspiderPipeline(object):
    def open_spider(self, spider):
        # 检查并创建文件夹（如果不存在）
        # 打开 CSV 文件以写入模式，并设置编码为 UTF-8
        self.file = open('sz.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)

        # 写入 CSV 文件头
        self.writer.writerow([
            'title', 'district',
            'area', 'direction',  'price','types'
        ])

    def close_spider(self, spider):
        # 爬虫关闭时关闭文件
        self.file.close()

    def process_item(self, item, spider):
        # 将每个 item 转换为列表形式并写入 CSV 文件
        row = [
            item['title'],
            item['district'],
            item['area'],
            item['direction'],
            item['price'],
            item['types']
        ]
        self.writer.writerow(row)
        return item