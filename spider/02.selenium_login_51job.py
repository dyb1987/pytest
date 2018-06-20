# -*- coding=utf8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

urladdr='https://login.51job.com/login.php'

driver_option = webdriver.ChromeOptions()
driver_option.add_argument("--headless")
driver_option.add_argument("--disable-gpu")
driver_option.binary_location = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
chromedrive=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver_win32\chromedriver.exe"

driver_explorer = webdriver.Chrome(chromedrive, chrome_options=driver_option)

driver_explorer.set_window_size(1280,1024)

driver_explorer.get("https://login.51job.com/login.php")
#
driver_explorer.implicitly_wait(5)

driver_explorer.save_screenshot("51job.png")

#输入用户名和密码
driver_explorer.find_element_by_id("loginname").send_keys("283931991@qq.com")
driver_explorer.find_element_by_id("password").send_keys("dengpwd,")

# 确认点击登录
driver_explorer.find_element_by_id('login_btn').click()
driver_explorer.find_element_by_class_name('p_but').click()
driver_explorer.implicitly_wait(3)
driver_explorer.save_screenshot("51job_new.png")

