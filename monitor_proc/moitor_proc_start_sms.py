#-*- coding:utf8 -*-
import configparser
import logging
import psutil
import os
import re
import subprocess
import time
import datetime
from logging.handlers import RotatingFileHandler
import monitorsms

#pyinstaller -F -w  --icon=apps.ico moitor_proc_start_sms.py

class MonitorCls(object):
    def __init__(self,configfile):
        self.procpath_list = []
        self.conf = configfile
        self.check_interval = 0
        self.mon_title = None
        self.proc_status = 0
        #self.proc_status_ok = 1
        self.workdir = ""
        self.pid_path_dict = {}
        self.status_list=[]

    def getconf(self):
        config = configparser.ConfigParser()
        config.read(self.conf,encoding='utf-8')
        # 读取配置
        # 获取 MonitorPath 中的监控路径，以列表的方式返回
        self.check_interval = config.get('checkrate','interval')
        self.mon_title = config.get('Title', 'title')
        #print(self.check_interval)
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

        log_file = RotatingFileHandler("./log/loginfo.log",maxBytes=52428800,backupCount=3) #maxBytes =50M,保留3份
        #log_file = logging.FileHandler("./log/loginfo.log")
        log_file.setLevel(logging.DEBUG)
        log_file.setFormatter(log_format)

        # 添加 handder
        monlog.addHandler(log_front)
        monlog.addHandler(log_file)
        monlog.info(logmsg)

        #  添加下面一句，在记录日志之后移除句柄，不然会重复打印 log 日志
        monlog.removeHandler(log_front)
        monlog.removeHandler(log_file)

    def check_status(self,fullpath, nametemp):
        proc_info_list = []
        path_list = []
        exe = nametemp
        # tasklist |findstr /C:"winbox" 说明:/C 后面接入的要过滤 出字符串
        run_cmd = "tasklist |findstr /C:" + exe
        tasklist1 = os.popen(run_cmd)
        # 获取 procstr 的格式如下：
        # winbox.exe                  131616 Console                    4     16,392 K
        # winbox.exe                  132060 Console                    4     16,496 K
        procstr = tasklist1.read()
        #print(procstr)
        # 如果没有找到进程 ，则字符串为 0
        if len(procstr) <1:
            self.proc_status = 0
            #print("进程不存在")
        else:
            my_re = re.compile(r"(.*.exe)\s+(\d+)", re.I) # re.I 忽略大小写
            re_res = re.findall(my_re, procstr)
            # re_res 格式为:[('winbox.exe', '131616'), ('winbox.exe', '132060')]
            for pname_temp, pid_temp in re_res:
                #print(pname_temp, pid_temp)
                p = psutil.Process(int(pid_temp))
                p_path = p.exe()
                proc_info_list.append((pid_temp, p_path))
                #结果为：[('131616', 'C:\\Users\\Administrator\\Desktop\\winbox.exe'), ('132060', 'D:\\py_test\\winbox.exe')]
                #print(proc_info_list)
                path_list.append(p_path)
            # print(path_list)
            if fullpath in path_list:
                self.proc_status = 1
            else:
                self.proc_status = 0
                #print("进程不存在2")
        return self.proc_status


    def process_check(self,procfullpath, procpathtemp, procnametemp):
        status = self.check_status(procfullpath, procnametemp)
        if status == 0:
            self.status_list.append(procfullpath)
            msgnew = "%s\%s  is shutdown..." % (procpathtemp, procnametemp)
            self.logger(msgnew)

            #  统计这个进程 在故障列表 self.status_list 里面出现了多少次，如果 小于等于 2 次 才发送短信，大于2 次就不发送短信了,
            # 同时每小时会重置 self.status_list， 为了避免 进程在1小时内，联系挂了超过  3  次
            # 只发送 每个进程判断 只发送 2次 短信

            if self.status_list.count(procfullpath) < 3:
                time.sleep(2)
                smscontent = "server:%s ; %s\%s is shutdown" % (self.mon_title, procpathtemp, procnametemp)
                monitorsms.smsSend(smscontent)

            time.sleep(2)
            # 启动进程
            os.chdir(procpathtemp)
            start_cmd = 'start ' + procpathtemp + "\\" + procnametemp
            # print(start_cmd)
            # subprocess 多线程的方式来启动相关进程；
            res = subprocess.Popen(start_cmd,shell=True)
            msgnew_info = "Restart process; %s\%s; %s  is starting..." % (procpathtemp, procnametemp, procnametemp)
            self.logger(msgnew_info)
            time.sleep(1)
            #print(msgnew_info)
            # 重新回到工作目录，去读取配置文件
            os.chdir(self.workdir)
        elif status == 1:
            msgnew = "%s\%s  is running..." % (procpathtemp, procnametemp)
            self.logger(msgnew)
            time.sleep(1)
            #print(msgnew)
        #print(self.status_list)
        # 执行 每小时 删除  self.status_list 列表里的数据
        now_min = datetime.datetime.now().minute
        if 10 < now_min < 13:
            del self.status_list[:]


    def procmon(self):
        # 获取 配置
        path_list = []
        config = self.getconf()
        for configtemp in config:
            #格式:('fpath1', 'd:\\py_test\\winbox.exe')
            path_list.append(configtemp[1])
        # print(path_list)

        for path in path_list:
            pathtemp = os.path.split(path)
            procpath, procname = pathtemp
            #将配置文件的路径和进程名，传给 检测函数，进行判断程序是否存在，将完整路径传给 process_check 函数
            self.process_check(procfullpath=path, procpathtemp=procpath,procnametemp=procname)

        #del self.status_list[:]


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
    msg_temp = "=="*30
    while True:
        mon.workdir = workdir
        mon.logger(msg_temp)
        mon.procmon()
        time.sleep(int(mon.check_interval))

