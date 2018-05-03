from urllib import request

header = {
   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
}

def urlopen(url,timeout_time,header):
    requestdata = request.Request(url,headers=header)
    resopnse = request.urlopen(requestdata,timeout=timeout_time)
    data = resopnse.read()

    # 返回 HTTP的响应码，成功返回200，4服务器页面出错，5服务器问题
    print(resopnse.getcode())

    # 返回 返回实际数据的实际URL，防止重定向问题
    print(resopnse.geturl())

    # 返回 服务器响应的HTTP报头
    print(resopnse.info())

    return data

baida_data = urlopen("https://www.cqmfin.com",10,header)

with open('./a.html','wb') as f:
    f.write(baida_data)
