# -*- coding=utf8 -*-
from threading import Thread
from queue import Queue
import random
import time

class handle_thread1(Thread):
    def __init__(self, tname, custqueue):
        super(handle_thread1, self).__init__()
        self.name = tname
        self.queue1 = custqueue

    def run(self):
        print("开始处理第一个队列数据,线程名为:%s" % self.name)
        self.cust_thread1()

    def cust_thread1(self):
        while self.queue1.qsize() > 0:
            num,url = self.queue1.get()
            print(num,url)
            time.sleep(2)
            cust_queue2.put(url)
        print("队列处理完成")




class handle_thread2(Thread):
    pass

global produce_queue1, cust_queue2
produce_queue1 = Queue()
cust_queue2 = Queue()

def mainfun():
    for x1 in range(1,100):
        put_args = (x1, "https://test/3179.html")
        # 往队列1 放入相关数据
        produce_queue1.put(put_args)
        time.sleep(1)

    prod_list = ['prod_thread1', 'prod_thread2', 'prod_thread3']
    for name in prod_list:
        prod = handle_thread1(name, produce_queue1)
        prod.start()

if __name__ == "__main__":
    mainfun()