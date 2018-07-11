#-*- coding:utf8 -*-

import os
import sys


if sys.platform == "win32":
    print("当前系统为windows")


git_user = "283931991@qq.com"
git_pwd = "ding082632"
git_mail = "283931991@qq.com"

class win_git_cls(object):
    def __init__(self, uname, upwd):
        self.name = uname
        self.pwd = upwd

    # 保存相关 git 配置
    def save_git_config(self):
        pass


if __name__ == "__main__":
    print(os.environ) # 获取执行用户的所有环境变量设置
    print(os.environ['USERPROFILE']) #获取 git 配置存储的目录