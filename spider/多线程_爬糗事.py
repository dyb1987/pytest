# 多线程爬虫 简单实现 步骤
# 创建 存储page 页面的队列 ——》 多线程爬取不同的页面 ——》 将爬取下来的 页面存入 队列里 data_quene ——》 多线程将 data_quene 里面的队列的数据 写入磁盘

# -*- coding:utf-8 -*-
import requests
from lxml import etree
from queue import Queue
import threading
import time
import json

class crawlThreadCls(threading.Thread): # 继承 threading 里的 Thread 类
    def __init__(self, threadid, pagequeue):
        super(crawlThreadCls,self).__init__() # 先调用父类的 初始化
        self.threadid = threadid
        self.queue = pagequeue
        # url_addr = 'https://www.qiushibaike.com/8hr/page/2/'

    def spider_data(self):
        while True:
            if self.queue.qsize() == 0: #如果队列为空 ，退出爬取动作
                break
            else:
                pagenum = self.queue.get()
                print('当前线程为：%s, 当前页面是第 %d 页' % (self.threadid, pagenum))
                url_addr = "https://www.qiushibaike.com/8hr/page/" + str(pagenum) +'/'
                header = {
                    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
                    'Accept-Language': 'zh-CN,zh;q=0.8'
                }
                # 多次尝试失败结束、防止死循环
                timeout = 4
                while timeout > 0:
                    timeout -= 1
                    try:
                        req_info = requests.get(url_addr,headers=header)

                        data_queue.put(req_info.text) #以 文本的 方式来获取 请求的文件内容，并放入队列中
                        break
                    except Exception as e:
                        print(e)
                if timeout < 0:
                    print('request url timeout %s' % url_addr)

class parserThreadCls(threading.Thread):
    pass



data_queue = Queue() #存放数据的队列
thread_lock = threading.Lock()

def main():
    output_file = open('qiushibaike.json', 'a')
    # 创建 页面队列 ，Queue() 没有接数字，表示没有设置队列 大小；
    page_queue = Queue()
    for num in range(1,11):
        page_queue.put(num)

    # 开始多线程 爬取页面
    # 定义 爬取的线程 存储列表， 和线程的名称
    crawl_threads = []
    crawl_list = ['crawl_thread1', 'crawl_thread2', 'crawl_thread3']

    for threadid in crawl_list:
        crawl_Thread = crawlThreadCls(threadid,page_queue)
        crawl_Thread.start()

        crawl_threads.append(crawl_Thread)

    # 初始化 分析 和 取出数据的 线程
    parser_threads = []
    parser_list = ["parser-thread1", "parser-thread2", "parser-thread3"]

    for parserid in parser_list:
        parser_thread_child = parserThreadCls(parserid, data_queue, thread_lock, output_file)


    # 等待队列清空 ，等待 获取页面的这个队列被清空了后再执行，分析数据的 线程；
    while not page_queue.empty():
        pass








    # 测试 从 page_queue 队列里面去数据

    # flag = True
    # while flag:
    #     print(page_queue.get())
    #     if page_queue.qsize() == 0:
    #         flag == False




if __name__ == "__main__":
    main()