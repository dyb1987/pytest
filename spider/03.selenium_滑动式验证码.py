# -*- coding=utf8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

url_addr = "http://192.168.1.150:12002/verify.html"
driver_dir = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

driver_option = webdriver.ChromeOptions()
driver_option.add_argument("--headless")
driver_option.add_argument("--disable-gpu")

driver_option.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

chrome_explorer = webdriver.Chrome(driver_dir, chrome_options=driver_option)

chrome_explorer.set_window_size(1024,720)
chrome_explorer.get(url_addr)

chrome_explorer.implicitly_wait(5)
# chrome_explorer.save_screenshot("first.png")

# 模拟鼠标拖动
mouse_drag = ActionChains(chrome_explorer)
#page_source = chrome_explorer.page_source

#drag_flag = chrome_explorer.find_element_by_class_name("handler")
drag_flag = chrome_explorer.find_element_by_xpath('//*[@class="handler handler_bg"]')

# 按住鼠标 左键
mouse_drag.click_and_hold(drag_flag).perform()
# 滑动坐标
mouse_drag.move_by_offset(250,0).perform()

# 释放鼠标
mouse_drag.release().perform()
chrome_explorer.save_screenshot("move1.png")


