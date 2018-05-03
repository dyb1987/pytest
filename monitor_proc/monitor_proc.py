#-*- coding:utf8 -*-

import configparser
import logging
import os

conf_file = "monitor.conf"
cfobj = configparser.ConfigParser()
cfobj.add_section('path2')
cfobj.set('path2', 'procname', 'zip.exe')

sec = cfobj.sections()
cfobj.read(conf_file)

res = cfobj.get('MonitorPath', 'fpath')
cfobj.write(open(conf_file, 'w'))

#打印日志
#设置日志名
applog = logging.getLogger("appserver-log")
#日志级别 #NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL
applog.setLevel(logging.DEBUG)

# 设置日志格式
log_format = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(filename)s[line:%(lineno)d] %(message)s')

#打印在前端 cmd
log_front = logging.StreamHandler()
log_front.setLevel(logging.INFO) #只在前端打印 info 级别的日志
log_front.setFormatter(log_format)

# 打印到 文件
if not os.path.exists("./log"):
    os.mkdir("./log")

log_file = logging.FileHandler("./log/loginfo.log")
log_file.setLevel(logging.DEBUG)
log_file.setFormatter(log_format)

##将相应的 handler 添加在logger对象中
applog.addHandler(log_front)
applog.addHandler(log_file)

msg = "sdfkjfksfjkjusfjkdsjf"
# 打印日志
# 打印什么级别的日志，这里的 info 是不能比 log_front.setLevel 这里设置的级别高，否则无法显示日志；
# 如果 log_front.setLevel 设置的是 debug ，那么这里 用info 是无法打印出来的；
applog.info('sdfkjfksfjkjusfjkdsjf')

