# -*- coding: utf-8 -*-
import scrapy
from myspider01.items import ItcastItem

class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['itcast.cn']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml',]

    def parse(self, response):

        items = []
        # filename = 'abc.txt'
        # source_data = response.body
        # with open(filename, "wb") as t_file:
        #     t_file.write(source_data)

        # 测试写入 数据到磁盘，是否正常
        for teacher in response.xpath('//*[@class="li_txt"]'):
            # 引用前面的数据封装到一个 `ItcastItem` 对象
            item_types = ItcastItem()
            # extract()方法返回的都是unicode字符串
            # text 获取标签里面的内容
            teacher_name = teacher.xpath('./h3/text()').extract()
            teacher_title = teacher.xpath('./h4/text()').extract()
            teacher_info = teacher.xpath('./p/text()').extract()

            # xpath返回的是包含一个元素的列表
            item_types['name'] = teacher_name[0]
            item_types['level'] = teacher_title[0]
            item_types['info'] = teacher_info[0]
            items.append(item_types)
            yield item_types



        #return(items)




