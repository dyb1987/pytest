#-*- coding:utf8 -*-

import os
import sys


curr_dir = os.getcwd()
cur_path = os.path.split(curr_dir)[1]


# 管理进程
def kill_proc(procid, proc_name):
    # 如果 传入的 proc_name 不等于 0；说明 是传入的进程名，然后执行相关操作
    if proc_name != '0':
        # 拼接命令
        procname = proc_name+'.exe'
        cmd_args = 'taskkill /im ' + procname + ' -f'
        # 执行关闭操作
        res = os.popen( cmd_args )
        # 输出处理结果
        print(res.read())
    elif procid != '0':
        cmd_args = 'taskkill /pid ' + procid + ' -f'
        res = os.popen( cmd_args )
        print(res.read())
    else:
        print("传入参数有误：pid:%s, pname:%s" % (procid, proc_name))

    # 注意，前者是按照exe名称杀进程的，会把同名的所有程序都杀死，比如你运行两个以上的python脚本，会把所有python脚本进程都杀死。
    # 后者是根据唯一的PID来杀的，准确安全

def start_proc_func():
    pass


if __name__ == "__main__":
    script_args = sys.argv
    try:
        if script_args[1] == '':
            print("请输入模块名")
    except Exception as e:
        print(e)
    else:
        #if script_args[2] == '':
        if len(script_args) < 3:
            print("请输入正确参数")
        else:
            args2 = script_args[2]
            # print(isinstance(args2, int)) 判断参数是否是 int 型
            # 如果参数2 是个数字 可能是个进程 号

            if args2.isdigit():
                procid = args2
                procname = '0'
            else:
                procid = '0'
                procname = args2

            if script_args[1] == "kill":
                kill_proc(procid=procid, proc_name=procname)