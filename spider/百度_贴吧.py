#coding:utf8
from urllib import request
import http.cookiejar
from urllib import parse
from lxml import etree
import random
from bs4 import BeautifulSoup
import requests
import os

# 定义 一个通用的加载页面 方法
def loadurl(url_addr):
    uagent_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 6.0.1; OPPO R9st Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043909 Mobile Safari/537.36 MicroMessenger/6.6.6.1300(0x26060632) NetType/WIFI Language/zh_CN",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.6.6 NetType/WIFI Language/zh_CN"

    ]
    request_header = {
        "User-Agent" : random.choice(uagent_list)
    }
    # 构建一个Session对象，可以保存页面Cookie
    req_session  = requests.Session()
    # 我们获取的是文档的数据，就用 text 如果是 发送图片的请求，获取图片数据流，就用 content
    # 同时测试发现 这个 get 还不能加 header 加了header 能获取到数据，但是通过 bs4 或者 xpath 转出 xml 后无法获取到URL
    req_data = req_session.get(url_addr).text
    return req_data
    # print(req_data)

# 下面这个方法是通过 urllib 的方式请求，测试发现些问题，通过 xpath 或者 bs4 无法获取的url
def request_func(url_addr):
    uagent_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 6.0.1; OPPO R9st Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043909 Mobile Safari/537.36 MicroMessenger/6.6.6.1300(0x26060632) NetType/WIFI Language/zh_CN",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.6.6 NetType/WIFI Language/zh_CN"

    ]
    request_header = {
        "User-Agent" : random.choice(uagent_list)
    }

    # 封装一个 cookie 保存回话
    cookie_data = http.cookiejar.CookieJar()
    cookie_handle = request.HTTPCookieProcessor(cookie_data)
    opener = request.build_opener(cookie_handle)

    # 封装request
    requestdata = request.Request(url_addr, headers=request_header)

    # 读取页面数据
    #responsedata = request.urlopen(requestdata, timeout=20).read()
    responsedata = opener.open(requestdata, timeout=20).read()
    data = responsedata.decode('utf8')
    print(data)
    bs_data = BeautifulSoup(data, 'lxml')
    tiezi_url_list = bs_data.find_all("a", attrs={"class":"j_th_tit"})

    print(tiezi_url_list)
    #return responsedata

def bs4_get_tiezi_url(urltemp):
    response_data = loadurl(urltemp)
    img_url_list = []
    # 下面2 行代码是通过 lxml 的 xpath 的方式
    # tiezi_content = etree.HTML(response_data)
    # tiezi_url_list1 = tiezi_content.xpath('//div[@class="threadlist_lz clearfix"]/div/a[@class="j_th_tit "]/@href')

    # 下面是通过 bs4 的方式进行匹配
    bs_data = BeautifulSoup(response_data, 'lxml')
    tiezi_url_data = bs_data.find_all("a", attrs={"class":"j_th_tit"})

    tiezi_url = "http://tieba.baidu.com"

    for data in tiezi_url_data:
        #tiezi_url_list.append(tiezi_url+data["href"])
        tiezi_full_url = tiezi_url+data["href"]

        # 抓取 每个帖子里面的图片
        # 先获取 这个页面的数据
        tiezi_data = loadurl(tiezi_full_url)

        #通过bs 4 去匹配图片的特征
        img_bs_data = BeautifulSoup(tiezi_data, 'lxml')
        img_url_data = img_bs_data.find_all('img',attrs={'class':'BDE_Image'})
        # 取出 页面路面并且 报错图片
        for img_url in img_url_data:
            img_url_list.append(img_url['src'])
            save_img(img_url['src'])

    #print(img_url_list)

def save_img(urldata):
    # 图片的地址，类似 https://imgsa.baidu.com/forum/w%3D580/sign=762446288b44ebf86d716437e9f9d736/9d35e5dde71190ef6b82edf4c21b9d16fdfa609b.jpg
    # 文件名
    filename = urldata[-10:]

    uagent_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36",
    ]
    request_header = {
        "User-Agent": random.choice(uagent_list)
    }
    imgdata = request.Request(urldata, headers=request_header)
    # 图片原始数据
    image = request.urlopen(imgdata).read()
    with open(filename, 'wb+') as f:
        f.write(image)
    print("已下载文件 %s" % urldata)


def start_spider(url_addr,spage,endpage,key_name):
    for page in range(spage, endpage+1):
        os.chdir(workdir) #切换到工作目录
        pn_num = (page - 1) * 50
        # 定义图片的存放目录
        dirname = key_name + "_" + str(page)
        if not os.path.exists(dirname):
            os.mkdir(dirname)
            os.chdir(dirname)
            url_temp = url_addr+"&pn="+str(page)
            print(url_temp)
            bs4_get_tiezi_url(url_temp)
        else:
            os.chdir(dirname)
            url_temp = url_addr+"&pn="+str(pn_num)
            bs4_get_tiezi_url(url_temp)


if __name__ == "__main__":
    search_key = input("请输入收缩关键字：")
    start_page = int(input("请输入爬取开始页："))
    end_page = int(input("请输入爬取结束页："))

    key_dict = {"kw": search_key}
    # 对输入的内容进行 urlcode 转码
    key = parse.urlencode(key_dict)
    ##https://tieba.baidu.com/f?kw=%E7%BE%8E%E5%A5%B3&pn=0  pn=0 是第几页
    url = "https://tieba.baidu.com/f?" + key
    global workdir
    workdir = os.getcwd()

    start_spider(url,start_page,end_page, search_key)

