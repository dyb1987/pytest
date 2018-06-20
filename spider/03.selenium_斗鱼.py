# -*- coding=utf8 -*-
'''
 抓取斗鱼直播的里面的 相关 评论数量 和作者
 https://www.douyu.com/directory/all  --这个页面点击下面的 分页，页面的地址是没有变化的
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re

urladdr='https://www.douyu.com/directory/all'

driver_option = webdriver.ChromeOptions()
driver_option.add_argument("--headless")
driver_option.add_argument("--disable-gpu")
driver_option.binary_location = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
chromedrive=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver_win32\chromedriver.exe"

driver_explorer = webdriver.Chrome(chromedrive, chrome_options=driver_option)

driver_explorer.set_window_size(1280,1024)

driver_explorer.get(urladdr)
# 显示页面等待处理；
driver_explorer.implicitly_wait(10)

# 尝试 访问 单页的 用户名和 该用户的关注 数

page_data = driver_explorer.page_source
#print(page_data)
data_bs_type = BeautifulSoup(page_data, 'lxml')

# 房间名, 返回列表
u_names = data_bs_type.find_all("h3", {"class":"ellipsis"})
# 观众人数, 返回列表
u_comment_nums = data_bs_type.find_all("span", {"class":"dy-num fr"})

global all_num
all_num = 0
# zip(u_names,u_comment_nums) 将name和number这两个列表合并为一个元组 : [(name1, number1), (name2, number2)...]
for uname, nums in zip(u_names,u_comment_nums):
    # \t 是关注和 房间名直接用 tab 隔开 ，同时 strip() 是去除空格
    number = nums.get_text().strip()
    uname_info = uname.get_text().strip()
    print("关注点播数： %s" % number + "\t 房间名称为: %s" % uname_info )
    # 结果类似：
        # 关注点播数： 6.9万	 房间名称为: 明早枪剑士直升满级装备毕业天空透明
        # 关注点播数： 6.9万	 房间名称为: Lilith：老球迷了！
        # 关注点播数： 7万	 房间名称为: 比赛都在用的套路，你不想看看吗
        # 关注点播数： 7万	 房间名称为: 今天小诗来济南啦
    #统计关注总人数:
    abc = re.findall('(\d+)(\.\d+)?', number)[0]
    number_new = abc[0] + abc[1]
    all_num += float(number_new)

# 如果在页面源码里找到"下一页"为隐藏的标签，就退出循环
# if self.driver.page_source.find("shark-pager-disable-next") != -1:
#     break

# 一直点击下一页
#self.driver.find_element_by_class_name("shark-pager-next").click()

print(all_num) # 结果4113.000000000003
