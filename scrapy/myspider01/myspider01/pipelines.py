# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class Myspider01Pipeline(object):
#     def process_item(self, item, spider):
#         return item
import json
class ItcastPipeline(object):
    def __init__(self):
        self.save_file = open("teacher2.json","wb")

    def process_item(self,item_data,spider):
        # 先将数据初始化成 字典类型，然后再 用 json 格式化存入
        item_dict = dict(item_data)
        item_json = json.dumps(item_dict, ensure_ascii=False) + "\n"
        # 把获取的item转换成utf-8编码
        self.save_file.write(item_json.encode("utf-8"))
        return item_json

    def close_spider(self,spider):
        self.save_file.close()