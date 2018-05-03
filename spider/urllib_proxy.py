#-*- conding=utf8 -*-
import random
from urllib import request,parse
import http.cookiejar

proxy_list = [
    {"http" : "222.76.187.56:8118"},
    {"http" : "222.76.187.56:8118"},
    {"http" : "222.76.187.56:8118"},
    {"http" : "222.76.187.56:8118"},
    {"http" : "222.76.187.56:8118"}
]

proxy_ip  = random.choice(proxy_list)

request_proxy = request.ProxyHandler(proxy_ip)
request_opener = request.build_opener(request_proxy)

# 构建一个CookieJar对象实例来保存cookie
cookie_data = http.cookiejar.CookieJar()
# 2. 使用HTTPCookieProcessor()来创建cookie处理器对象，参数为CookieJar()对象
cookie_hanndle = request.HTTPCookieProcessor(cookie_data)

login_data = {
    "loginname":"sdfdf",
    "password":""
}
postdata = parse.urlencode(login_data).encode(encoding='utf-8')

opener = request.build_opener(cookie_hanndle)

url_addr = "https://login.51job.com/login.php?lang=c&url=http%3A%2F%2Fwww.51job.com%2F"
request_info = request.Request(url=url_addr,data=postdata)

requestdata_all = opener.open(request_info)

#requestdata_all = opener.open("https://i.51job.com/resume/resume_center.php?lang=c")

print(requestdata_all.read())