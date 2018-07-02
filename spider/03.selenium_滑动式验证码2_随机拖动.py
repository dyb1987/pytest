# -*- coding=utf8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import random

class drag_verify_code(object):
    def __init__(self):
        self.url_addr = "http://192.168.1.150:12002/verify.html"
        self.driver_dir = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

        self.driver_option = webdriver.ChromeOptions()
        self.driver_option.add_argument("--headless")
        self.driver_option.add_argument("--disable-gpu")

        self.driver_option.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

        self.chrome_explorer = webdriver.Chrome(self.driver_dir, chrome_options=self.driver_option)
        self.chrome_explorer.set_window_size(1024, 720)

    def start_verify(self):
        self.chrome_explorer.get(self.url_addr)
        self.chrome_explorer.implicitly_wait(5)
        # 创建鼠标动作
        mouse_drag = ActionChains(self.chrome_explorer)

        # 捕获 要点击的 内容
        drag_flag = self.chrome_explorer.find_element_by_xpath('//*[@class="handler handler_bg"]')
        # 按住鼠标 左键
        mouse_drag.click_and_hold(drag_flag).perform()

        # 随机动态 移动 鼠标位置
        num = 0
        while num < 20:
            num += random.randint(1, 50)
            mouse_drag.move_by_offset(num, 0).perform()

        self.chrome_explorer.save_screenshot('moved.png')
        # 释放鼠标
        mouse_drag.release()


if __name__ == '__main__':
    drag_verify_code().start_verify()



