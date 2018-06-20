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

    def run(self):
        print("开始下载数据；")
        self.spider_data()

    def spider_data(self):
        global crawl_flag
        if self.queue.empty() == True:
            crawl_flag = False
            print("网页下载队列，已空")
        else:
            crawl_flag = True
        while crawl_flag:
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
                        #data = req_info.text.decode('utf8')
                        data_queue.put(req_info.text) # text 方法是以 文本的 方式来获取 请求的文件内容，并放入队列中
                        break
                    except Exception as e:
                        print(e)
                if timeout < 0:
                    print('request url timeout %s' % url_addr)

class parserThreadCls(threading.Thread):
    def __init__(self, parserid, data_queue, datalock, store_file):
        super(parserThreadCls, self).__init__()
        self.parserid = parserid
        self.data_q = data_queue
        self.datalock = datalock
        self.store_file = store_file

    def run(self):
        print("开始分析获取数据")
        global parser_flag
        while not parser_flag:
            try:
                # 在队列  block =  True(默认) 和 timeout 两个参数，当  block = True 时，写入和读取 是阻塞式的，阻塞时间由 timeout  确定
                # Queue.get（）默认的也是阻塞方式读取数据，队列为空时，不会抛出 except Queue.Empty ，而是进入阻塞直至超时。 加上 block=False 的参数;
                # 如果队列为空且block为False，队列将引发 Empty 异常;
                page_data = self.data_q.get(block=False)
                data_temp = page_data.encode('utf-8')
                self.parserdata(page_data)
                self.data_q.task_done()
                print('分析数据线程为：%s, 已完成工作' % self.parserid)

            except Exception as err:
                print(err)

        print('完成数据分析,线程是：%s' % self.parserid)


    def parserdata(self, htmldata):

        try:
            # htmldata_temp = htmldata.decode('utf8')
            xmldata = etree.HTML(htmldata)
            all_tiezi = xmldata.xpath('//div[contains(@id,"qiushi_tag_")]') # 获取所有的段子的 标签和内容部分
            for tiezi_detail in all_tiezi:
                try:
                    imgUrl = tiezi_detail.xpath('.//img/@src')[0]
                    title = tiezi_detail.xpath('.//h2')[0].text
                    content = tiezi_detail.xpath('.//div[@class="content"]/span')[0].text.strip()
                    vote = None
                    comments = None
                    try:
                        vote = tiezi_detail.xpath('.//i')[0].text
                        comments = tiezi_detail.xpath('.//i')[1].text
                    except:
                        pass

                    tiezi_data = {
                        'imgUrl': imgUrl,
                        'title': title,
                        'content': content,
                        'vote': vote,
                        'comments': comments,
                    }
                    #print(tiezi_data)
                    #writedate = tiezi_data
                    with self.datalock:
                        # 这里取出来的数据是 bytes 类型的，加了个换行符 \n 也需要转换成 bytes 类型的
                        self.store_file.write(json.dumps(tiezi_data,ensure_ascii=False).encode('utf-8') + "\n".encode(encoding='utf8'))
                except Exception as err:
                    print(err)

        except Exception as Err:
            print(Err)


global data_queue
data_queue = Queue() #存放数据的队列
thread_lock = threading.Lock()
global parser_flag
parser_flag = False

def main():
    output_file = open('qiushibaike.json', 'wb+')
    # 创建 页面队列 ，Queue() 没有接数字，表示没有设置队列 大小；
    page_queue = Queue()
    for num in range(1,4):
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

    # 开始 分析 页面的 相关 数据信息的线程

    for parserid in parser_list:
        parser_thread_child = parserThreadCls(parserid, data_queue, thread_lock, output_file)
        parser_thread_child.start()
        parser_threads.append(parser_thread_child)

    # 等待队列清空 ，等待 获取页面的这个队列被清空了后再执行，分析数据的 线程；
    while not page_queue.empty():
        #print(1)
        pass
    # 添加 join 功能，防止 主进程 退出，子线程 退出；
    for crawl_thread_join in crawl_threads:
        crawl_thread_join.join()
    # print(data_queue.qsize())

    while not data_queue.empty():
        pass
    global parser_flag
    parser_flag = True
    for parser_thread_join in parser_threads:
        parser_thread_join.join()
    with thread_lock:
        output_file.close()



    # 测试 从 page_queue 队列里面去数据

    # flag = True
    # while flag:
    #     print(page_queue.get())
    #     if page_queue.qsize() == 0:
    #         flag == False

if __name__ == "__main__":
    main()