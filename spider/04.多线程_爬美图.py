# -*- conding=utf8 -*-

from threading import Thread
from queue import Queue
import random
from bs4 import BeautifulSoup
from lxml import etree
import requests
import os

class handel_main_url(Thread):
    def __init__(self,thread_name, queue_name):
        super(handel_main_url, self).__init__()
        self.thread_name = thread_name
        self.queue_name = queue_name

    def handel_main_url_func(self):
        print("当前线程为: %s ； 正在处理 主页面数据"  % self.thread_name)

        # 从队列中取出 美女 名称和 美女主页面
        while self.queue_name.qsize()>0:
            gname, gmain_url = self.queue_name.get() # 从队列中取数据

            # 开始获取 每个美女 主页 的子页面url
            request_header = {
                'User-Agent': "Mozilla/5.0",
                "Referer": "http://www.baidu.com"
            }
            try:
                req_main_info = requests.get(gmain_url,headers=request_header)
            except Exception as err:
                print("%s 访问地址异常;异常信息为: %s" % (gmain_url, err))

            # 我通过 lxml etree 来处理

            xml_type = etree.HTML(req_main_info.content)
            """
            <div id="pages"><a class="a1" href="/item/14145.html">上一页</a> <span>1</span> <a href="/item/14145_2.html">2</a> 
            <a href="/item/14145_3.html">3</a> <a href="/item/14145_4.html">4</a> <a href="/item/14145_5.html">5</a> 
            <a href="/item/14145_6.html">6</a> <a href="/item/14145_7.html">7</a> 
            <a href="/item/14145_8.html">8</a> <a href="/item/14145_9.html">9</a> 
            <a href="/item/14145_10.html">10</a> ..<a href="/item/14145_22.html">22</a> 
            <a class="a1" href="/item/14145_2.html">下一页</a></div>
            我觉得 应该取出 22 这个页面来表示 这个主页 有多少 个子页面
            """
            xml_data = xml_type.xpath('//div[@id="pages"]/a')
            temp_main_url = gmain_url.split(".html")[0] # https://www.meitulu.com/item/14456 获取主页面
            child_url_list = []
            num_list = [] # 结果类似 ['上一页', '2', '3', '4', '5', '6', '7', '8', '9', '10', '15', '下一页']
            for temp in xml_data:
                tempnum = temp.text
                #print(tempnum)
                num_list.append(tempnum)

            #print(num_list)
            last_url = num_list[-2] #获取 列表的第二个值
            i = 1
            child_url_list.append(gmain_url)
            while i < int(last_url):
                i += 1
                child_url = temp_main_url+"_"+str(i)+".html" #重新拼接 子 URL
                child_url_list.append(child_url)
            child_url_tumple = (gname, child_url_list)
            # 结果类似:
            # ('[XIUREN秀人网] No.976 高挑美女@呆呆的瑞bb第二套写真', ['https://www.meitulu.com/item/14463.html',
            # 'https://www.meitulu.com/item/14463_2.html', 'https://www.meitulu.com/item/14463_3.html', 'https://www.meitulu.com/item/14463_4.html'......])
            # print(child_url_tumple)
            # 将这些子页面加入到列表中
            meizi_img_url_queue.put(child_url_tumple)

    def run(self):
        self.handel_main_url_func()

class handel_detail_url(Thread):
    def __init__(self,threadname, queuename):
        super(handel_detail_url, self).__init__()
        self.thread_name = threadname
        self.queue_name = queuename

    def handel_child_url(self):
        print("开始处理 美女 子页面")
        while self.queue_name.qsize() > 0:
            girl_name, girl_child_url_list = self.queue_name.get()
            #print(girl_name,girl_child_url_list)
            for child_url in girl_child_url_list:
                #print(girl_name)
                self.get_child_img_url(girl_name, child_url)

    def get_child_img_url(self,girl_name,main_url):
        request_header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
            "Referer": main_url
        }
        img_info = requests.get(main_url, headers=request_header)
        xml_data = etree.HTML(img_info.content)
        for imgurl in xml_data.xpath('//div[@class="content"]//img/@src'):
            print("开始下载图片:%s" % imgurl)
            self.down_img(girl_name,main_url,imgurl)

    def down_img(self,girl_name,main_url, img_url):
        if not  os.path.exists(savedir):
            os.makedirs(savedir)
            os.chdir(savedir)
        else:
            os.chdir(savedir)

        if not os.path.exists(girl_name):
            os.makedirs(girl_name)
            os.chdir(girl_name)
        else:
            os.chdir(girl_name)

        request_header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
            "Referer": main_url
        }
        file_name = img_url.split('/')[-1]
        img_data = requests.get(img_url,headers=request_header)
        with open(file_name,'wb') as f:
            f.write(img_data.content)
        print("下载图片成功")

    def run(self):
        self.handel_child_url()



global meizi_main_queue, meizi_img_url_queue, savedir

meizi_main_queue = Queue()
meizi_img_url_queue = Queue()
savedir = r"E:\back"


def main_func():
    url_addr_main = "https://www.meitulu.com/"

    request_header = {
        'User-Agent': "Mozilla/5.0",
        "Referer": "http://www.baidu.com"
    }
    try:
        req_info = requests.get(url_addr_main,headers=request_header)
        req_info.raise_for_status()
        req_info.encoding=req_info.apparent_encoding
        #reqdata = req_info.text()
        # print(req_info.text)  # 打印整个首页
    except:
        print("访问https://www.meitulu.com 异常")

    soup_data = BeautifulSoup(req_info.content, "lxml")
    bsdata = soup_data.find_all("p",{"class":"p_title"})
    # 内容为一个列表 [<p class="p_title"><a href="https://www.meitulu.com/item/12433.html" target="_blank">[Kimoe激萌文化] KIM014 周闻 - 球球穿毛衣变身小可爱沙漠之旅</a></p>,
    # <p class="p_title"><a href="https://www.meitulu.com/item/9447.html" target="_blank">[XiuRen秀人网] No.648 尤Una娜 - 首套写真</a></p>......]
    for data in soup_data.find_all("p",{"class":"p_title"}):
        girl_name = data.string # 获取  每个主页图片的名字
        girl_mail_url = data.find('a')['href'] # 获取 href 中的链接地址
        meizi_main_queue.put((girl_name,girl_mail_url))
        #print(girl_name, girl_mail_url)
    #print(bsdata)

    # 多线程处理 首页，并获取 每个美女的 子页面 链接
    meizi_main_thread_name_list = ["mail_url_thread1", "mail_url_thread2", "mail_url_thread3","mail_url_thread4","mail_url_thread5" ]
    meizi_main_thread_list = []
    for tname in meizi_main_thread_name_list:
        main_url_thread = handel_main_url(tname, meizi_main_queue)
        main_url_thread.start()
        meizi_main_thread_list.append(main_url_thread)

    while not meizi_main_queue.empty():
        pass

    for mthread in meizi_main_thread_list:
        mthread.join()

    meizi_child_thread_name_list = ["girl_child_url_threa1", "girl_child_url_threa2", "girl_child_url_threa3","girl_child_url_threa4","girl_child_url_threa5" ]
    meizi_child_thread_list = []
    for child_tname in  meizi_child_thread_name_list:
        child_url_thread = handel_detail_url(child_tname,meizi_img_url_queue)
        child_url_thread.start()
        meizi_child_thread_list.append(child_url_thread)

    while not meizi_img_url_queue.empty():
        pass

    for child_tread in meizi_child_thread_list:
        child_tread.join()




if __name__ == "__main__":
    main_func()
