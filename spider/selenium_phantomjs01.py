# 单纯导入 selenium 的 webdrive 包
from selenium import webdriver
import time

# 要想调用键盘按键操作需要引入keys包
from selenium.webdriver.common.keys import Keys

driver_option = webdriver.ChromeOptions()
driver_option.add_argument('--headless')
driver_option.add_argument('--disable-gpu')
driver_option.binary_location = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
# chrome_options.binary_location = '/opt/google/chrome/chrome'
chromedrive=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver_win32\chromedriver.exe"
#driver_explorer = webdriver.PhantomJS(executable_path="c:/tools/phantomjs/bin/phantomjs.exe")
driver_explorer = webdriver.Chrome(chromedrive, chrome_options=driver_option)

driver_explorer.get("http://www.baidu.com")

#print(driver_explorer.title) # 获取标题
#print(driver_explorer.get_cookies()) # 获取cooke s

# 获取页面名为 wrapper的id标签的文本内容
#data = driver_explorer.find_element_by_id("wrapper").text
# 打印数据内容
#print(data)

# 获取页面名， 并对id 为 kw 的标签，发送的文本内容
driver_explorer.find_element_by_id("kw").send_keys(u'测试')
driver_explorer.find_element_by_id("su").send_keys(Keys.RETURN) #对这个ID 发送回车 符 ，操作
time.sleep(1)
driver_explorer.find_element_by_id("su").click() #对这个ID ,模拟鼠标单击操作

driver_explorer.save_screenshot('baidu.png')
