#-*- coding:utf8 -*-
import configparser
import logging
import psutil
import os
import re
import subprocess
import time

class MonitorCls(object):
    def __init__(self,configfile):
        self.procpath_list = []
        self.conf = configfile
        self.check_interval = 0
        self.proc_status = 0
        self.workdir = ""
        self.pid_path_dict = {}

    def getconf(self):
        config = configparser.ConfigParser()
        config.read(self.conf)
        # 读取配置
        # 获取 MonitorPath 中的监控路径，以列表的方式返回
        self.check_interval = config.get('checkrate','interval')
        print(self.check_interval)
        configdata = config.items('MonitorPath')
        return configdata

    def logger(self, logmsg):
        # 定义日志对象
        monlog = logging.getLogger("monitor_log")
        monlog.setLevel(logging.DEBUG)

        # 设置日志格式
        log_format = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(filename)s[line:%(lineno)d] %(message)s')

        # 打印到前端
        log_front = logging.StreamHandler()
        log_front.setLevel(logging.DEBUG)
        log_front.setFormatter(log_format)

        #打印日志到文件
        if not os.path.exists("./log"):
            os.mkdir("./log")

        log_file = logging.FileHandler("./log/loginfo.log")
        log_file.setLevel(logging.DEBUG)
        log_file.setFormatter(log_format)

        # 添加 handder
        monlog.addHandler(log_front)
        monlog.addHandler(log_file)
        monlog.info(logmsg)

        #  添加下面一句，在记录日志之后移除句柄，不然会重复打印 log 日志
        monlog.removeHandler(log_front)
        monlog.removeHandler(log_file)

    #def get_pid(self,procpathtemp, procnametemp):


    def process_check(self,procfullpath, procpathtemp, procnametemp):
        print(procfullpath, procpathtemp, procnametemp)
        allproc = psutil.process_iter()
        #将所有进程名，加入到列表中

        for proc in allproc:
            procnew = str(proc) # 格式化成字符串，格式为：psutil.Process(pid=95048, name='winbox.exe', started='11:18:14')
            procnamenew = re.search(procnametemp, procnew, re.I)
            # print(procnamenew)
            if procnamenew:
                # 如果 在进程中能 search 到 进程名：
                proc_pid = re.findall('pid=(\d+)',procnew)[0] #通过进程名，获取找到的进程ID ,结果如：95048
                # print(proc_pid)
                # 获取这个进程的目录
                p = psutil.Process(int(proc_pid))
                pid_path = p.exe()
                # 先在 self.pid_path_dict 字典中查找是否有 pid 存在，如果不存在就 将 pid 和pid_path 存入字典中
                # 如果没有在字典中就返回 None
                pid_path_dict_temp = self.pid_path_dict.get(proc_pid,None)

                if pid_path_dict_temp == None :
                    self.proc_status = 0
                    self.pid_path_dict[proc_pid] = (proc_pid, pid_path)
                    print(self.pid_path_dict)
                else:
                    self.proc_status = 1



                # 如果 当前进程的 exe 路径， 如: D:\py_test\winbox.exe 没在 self.procpath_list 中，就加进去
                # if pid_path not in self.procpath_list:
                #     self.procpath_list.append(pid_path)
                #
                # print(self.procpath_list, proc_pid, pid_path, procpathtemp)

                #如果 传入 从配置文件中获取的完整路径，在 self.procpath_list 中的话，那么表示程序在运行；
                # if procfullpath in self.procpath_list:
                #     self.proc_status = "1"
                #     msgnew = "%s\%s  is running..." % (procpathtemp, procnametemp)
                #     self.logger(msgnew)
                #     time.sleep(1)
                # else:
                #     self.procpath_list.append(procfullpath)
                #     self.proc_status = 0
            else:
                self.proc_status = 0

        if self.proc_status == 0:
            msgnew = "%s\%s  is shutdown..." % (procpathtemp, procnametemp)
            self.logger(msgnew)

            # 启动进程
            os.chdir(procpathtemp)
            start_cmd = 'start ' + procpathtemp + "\\" + procnametemp
            # print(start_cmd)
            # subprocess 多线程的方式来启动相关进程；
            #res = subprocess.Popen(start_cmd,shell=True)
            msgnew_info = "Restart process; %s\%s; %s  is starting..." % (procpathtemp, procnametemp, procnametemp)
            self.logger(msgnew_info)
            time.sleep(1)
            #print(msgnew_info)
            # 重新回到工作目录，去读取配置文件
            os.chdir(self.workdir)

            # 将进程 信息放入字典中
            # proc_all_temp = psutil.process_iter()
            # for proc_temp in proc_all_temp:
            #     proc_temp_new = str(proc_temp) #格式化成字符串，格式为：psutil.Process(pid=95048, name='winbox.exe', started='11:18:14')
            #     proctempnew = re.search(procnametemp, proc_temp_new, re.I)
            #     if proctempnew:
            #         # 如果 在进程中能 search 到 进程名：
            #         proc_pid = re.findall('pid=(\d+)', proc_temp_new)[0]
            #         #print(proc_pid)
            #         if proc_pid :
            #             self.pid_path_dict[proc_pid] = procfullpath
            #     print(self.pid_path_dict)


        # if self.proc_status == "1":
        #     msgnew = "%s\%s  is running..." % (procpathtemp, procnametemp)
        #     self.logger(msgnew)
        #     time.sleep(1)
        #     #print(msgnew)
        # elif self.proc_status == 0:
        #     msgnew = "%s\%s  is shutdown..." % (procpathtemp, procnametemp)
        #     self.logger(msgnew)
        #     #print(msgnew)
        #
        #     os.chdir(procpathtemp)
        #     start_cmd = 'start ' + procpathtemp + "\\" + procnametemp
        #     # print(start_cmd)
        #     # subprocess 多线程的方式来启动相关进程；
        #     res = subprocess.Popen(start_cmd,shell=True)
        #     msgnew_info = "Restart process; %s\%s; %s  is starting..." % (procpathtemp, procnametemp, procnametemp)
        #     self.logger(msgnew_info)
        #     time.sleep(1)
        #     #print(msgnew_info)
        #     os.chdir(self.workdir)



    def procmon(self):
        # 获取 配置
        path_list = []
        config = self.getconf()
        for configtemp in config:
            #格式:('fpath1', 'd:\\py_test\\winbox.exe')
            path_list.append(configtemp[1])

        for path in path_list:
            pathtemp = os.path.split(path)
            procpath, procname = pathtemp
            #将配置文件的路径和进程名，传给 检测函数，进行判断程序是否存在，将完整路径传给 process_check 函数
            self.process_check(procfullpath=path, procpathtemp=procpath,procnametemp=procname)

        #del self.procpath_list[:]



if __name__ == "__main__":
    workdir = os.getcwd()
    config_file = "./monitor.conf"

    mon = MonitorCls(config_file)
    if not os.path.exists(config_file):
        msg = "%s config file does not exist. 配置文件不存在" % config_file
        mon.logger(msg)
        exit(1)

    # 读取一次配置文件，从配置中获取检测的间隔时间
    mon.conf
    while True:
        mon.workdir = workdir
        mon.procmon()
        time.sleep(int(mon.check_interval))







