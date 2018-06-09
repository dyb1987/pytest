import json
import jsonpath
from urllib import request
import random
from urllib.parse import urlencode

url_addr = 'http://www.lagou.com/lbs/getAllCitySearchLabels.json'

uagent_list = [
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)"
    ]
u_agent =  {
        'User-Agent':random.choice(uagent_list)
}
request_data = request.Request(url_addr,headers=u_agent)

url_open = request.urlopen(url_addr)

# 获取网页的数据，并且 将数据格式转换为 utf 8 格式
data = url_open.read().decode('utf8')

# 将数据转成 json 数据
json_data = json.loads(data)

#通过 jsonpath 获取 城市数据 其中 $..name 的意思： 从根开始查找 匹配 所有 位置的 name 字段；
city_list = jsonpath.jsonpath(json_data, '$..name')
#print(city_list)

# 将 数据 写入 磁盘

city_file = open('city_file.txt','w+')
content = json.dumps(city_list,ensure_ascii=False)
city_file.write(content)
city_file.close()