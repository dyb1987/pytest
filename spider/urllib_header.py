from urllib import request,parse
import random




def load_url(url,pagename):
    print("正在加载下载第 %s 页面................" % pagename)
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

    #随意选择个 浏览器代理
    uagent = {
        'User-Agent': random.choice(uagent_list)
    }
    # 封装request
    requestdata = request.Request(url,headers=uagent)
    # 读取页面数据
    responsedata = request.urlopen(requestdata,timeout=20).read()
    return responsedata

def write_html(filename,data):
    print("这种写盘数据 %s ....." % filename)
    with open(filename, 'wb') as f:
        f.write(data)


def init_url(url, startpage, endpage, key_name):

    for page in range(startpage,endpage+1):
        pn = str(page * 50)
        newurl = url+"&pn="+pn
        #组装 名称
        pagename = key_name+"_"+str(page)+".html"
        #print(newurl)
        #调用获取数据的函数
        getdata = load_url(newurl, pagename)
        write_html(pagename,getdata)

if __name__ == "__main__":
    search_key = input("请输入收缩关键字：")
    start_page = int(input("请输入爬取开始页："))
    end_page = int(input("请输入爬取结束页："))
    key_dict = {"kw":search_key}
    key = parse.urlencode(key_dict)
    url = "https://tieba.baidu.com/f?" + key
    init_url(url, startpage=start_page, endpage=end_page,key_name=search_key)