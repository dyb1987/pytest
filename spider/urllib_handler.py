#-*- conding=utf8 -*-
import random
from urllib import request

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
        'User-Agent': random.choice(uagent_list)
}



# 重新定义 HTTP 请求对象，这个对象可以自定义一些请求方式
http_handler = request.HTTPHandler()

# 对自定义的 handler 进行封装
http_opener = request.build_opener(http_handler)

# 对请求封装
url_addr = "https://www.baidu.com"
request_info = request.Request(url=url_addr,headers=request_header)

# 通过 opener 的open 方法请求数据
request_data = http_opener.open(request_info)
print(request_data.read())



