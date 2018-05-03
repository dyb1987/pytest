#conding:utf8
from urllib import request,parse
import re
import random
import os

class spderDuanzi():
    def __init__(self):
        self.page_num = 2
        self.flag = True
        #print(self.page_url)

    def downpage(self):
        page_url = "http://www.neihanpa.com/wenzi/index_" + str(self.page_num) + ".html"
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
        request_headers = {
            'User-Agent': random.choice(uagent_list)
        }

        request_info = request.Request(url=page_url,headers=request_headers)
        request_data = request.urlopen(request_info).read().decode('utf8')
        #print(request_data)

        re_title = re.compile(r'<div class="text-column-item box box-790">([\s\S]*?</div>)')
        title_content = re_title.findall(request_data, re.I)
        #print(title_content)
        #print(type(title_content))
        self.dealpage(title_content)

    # 处理 页面中段子的数据，取出title 和 title对应的内容
    def dealpage(self,content):
        for data in content:
            title_temp = re.findall(r'title=(.*?)>',data,re.S)
            content_temp = re.findall(r'<div class="desc">(.*?)</div>', data, re.S)
            # 格式 为:
            #['"他还想吃"']
            #[
            #    ' \u3000\u3000约翰从学校带了黑眼圈回家，妈妈问这是怎么回事，约翰答道：“我跟比尔打了一架。”\u3000\u3000妈妈明理地说：“明天你带块蛋糕给比尔，并向他道歉。”\u3000\u3000第二天约翰又带回一个更大的']
            #print(title_temp,content_temp)
            title = title_temp[0].replace('\"',"") #去掉 title 的引号
            try:
                self.saveduanzi(title)
                self.saveduanzi(content_temp[0])
                msg_temp = "==" * 30
                self.saveduanzi(msg_temp)
            except Exception as msg:
                print(msg)
            #break


    def saveduanzi(self,data):
        file = "duanzi"+str(self.page_num)+".txt"
        # if os.path.exists(file):
        #     os.remove(file)

        with open(file, 'a+') as f:
            f.write(data)
            f.write('\r\n')

    def startspider(self):
        while self.flag:
            self.downpage()
            command = input("如果继续爬取，请按回车（退出输入quit)")
            if command == "quit":
                self.flag = False
            self.page_num += 1
        print("谢谢使用")

if __name__ == "__main__":
    get_dz = spderDuanzi()
    get_dz.startspider()