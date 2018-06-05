#coding:utf8

import hashlib
from urllib import request
from urllib import parse
import configparser
import os
import json

global workdir
workdir = os.getcwd()

def smd5(str_args):
    str_hash = hashlib.md5()
    str_hash.update(str_args.encode('utf8'))
    return str_hash.hexdigest()


def sendmsg(account, pswd, content, mobile):
    """
    发送短信
    """
    smsapi = "http://api.smsbao.com/"
    statusStr = {
        '0': '短信发送成功',
        '-1': '参数不全',
        '-2': '服务器空间不支持,请确认支持curl或者fsocket,联系您的空间商解决或者更换空间',
        '30': '密码错误',
        '40': '账号不存在',
        '41': '余额不足',
        '42': '账户已过期',
        '43': 'IP地址限制',
        '50': '内容含有敏感词'
    }

    params = parse.urlencode({'u': account, 'p': pswd, 'm': mobile, 'c': content})
    req_headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    send_url = smsapi + 'sms?' + params
    req_data = request.Request(send_url, headers=req_headers)
    response = request.urlopen(req_data)

    page = response.read().decode('utf-8')

    print(statusStr[page])

def get_conf_phone(conffile):
    phone_list = []
    conf = configparser.ConfigParser()
    conf.read(conffile, encoding='utf-8')
    smsbutton = conf.get('smsbutton','button')

    # 读取配置
    # 获取 MonitorPath 中的监控路径，以列表的方式返回
    phone_data = conf.items('smsphone')
    for name, phone in phone_data:
        phone_list.append(phone)
    #print(phone_list)
    return phone_list,smsbutton

def smsSend(contenttemp):
    # 短信平台账号
    user = 'xianyu'
    # 短信平台密码
    password = smd5('sms153pwdXianyu')
    # 要发送的短信内容
    content = '【重庆闲娱科技有限公司】 尊敬的用户: %s ; 退订回N ' % contenttemp
    # 要发送短信的手机号码
    os.chdir(workdir)
    conf_file = './sms.conf'
    phone, button = get_conf_phone(conf_file)
    for phonetemp in phone:
        # 如果 配置文件的 发送短信开启，表示可以发送短信
        if button == '1':
            sendmsg(user, password, content, phonetemp)
        else:
            print("发送短信给：%s 主题: %s" % (phonetemp, content))


if __name__ == "__main__":
    smsSend("test123")


