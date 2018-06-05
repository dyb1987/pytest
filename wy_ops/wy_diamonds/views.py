from django.shortcuts import render
from django.http import *
from django.template import loader,RequestContext
from .models import *
import pymysql
# Create your views here.

def index(request):
    return render(request, 'diamonds/index.html')

db_info = {
        'host': '192.168.56.10',
        'user': 'root',
        'password': '1234567',
        'db': 'gamedb_xsbh',
        'port': 3306,
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
    }

def getdata(exec_sql):
    db_connect = pymysql.connect(**db_info)

    db_cursor = db_connect.cursor()
    try:
        db_cursor.execute(exec_sql)
        get_data = db_cursor.fetchall()
    except Exception as error_msg:
        print(error_msg)
    finally:
        db_cursor.close()
        db_connect.close()
    return get_data

def changedata(exec_sql):
    db_connect = pymysql.connect(**db_info)

    db_cursor = db_connect.cursor()
    try:
        db_cursor.execute(exec_sql)
        db_connect.commit()
    except Exception as error_msg:
        print(error_msg)
    finally:
        db_cursor.close()
        db_connect.close()

def displayinfo(request):
    dis_uid = request.POST.get('inputdispayid')
    if dis_uid is None:
        print("please use post method to post data")
        exit(1)
    else:
        role_id = int(dis_uid)^20517

    exec_sql = 'SELECT ROLEID,ACCOUNTID,MONEY,RMB,`NAME`,FROM_UNIXTIME(LASTOFFLINETIME) as offtime from t_role WHERE roleid = %s'% (str(role_id))
    data = getdata(exec_sql)
    # 数据类似： [{'NAME': '红枫叶', 'ROLEID': 1, 'RMB': 0, 'MONEY': 12500, 'ACCOUNTID': 1, 'FROM_UNIXTIME(LASTOFFLINETIME)': datetime.datetime(2018, 5, 25, 11, 30, 27)}]

    if len(data) < 1:
        print("don't get any data")
    elif len(data) == 1:
        data_dict = data[0] #取出 数据里面的字段
    else:
        print("get many data")
        print(data)
        data_dict = data[0]
    #print(data,data_dict.get('offtime'))
    html_data = {
        'disid': dis_uid,
        'roleid': role_id,
        'ACCOUNTID': data_dict.get('ACCOUNTID'),
        'disname': data_dict.get('NAME'),
        'dismoney': data_dict.get('MONEY'),
        'disrmb': data_dict.get('RMB'),
        'lastofftime': str(data_dict.get('offtime'))
    }

    return render(request,'diamonds/displayinfo.html', html_data)

def changermb(request):
    dis_uid = request.POST.get('changeuserid')
    add_diamonds = request.POST.get('adddiamond')
    if dis_uid is None:
        print("please use post method to post data")
        exit(1)
    else:
        role_id = int(dis_uid)^20517

    if role_id == '':
        print("Change rmd didn't get role ID,exit")
        exit(2)
    else:
        # 先获取当前数据库的 rmb 信息，然后写入 日志 rmb_change_info 表中
        pre_select_sql = 'SELECT ROLEID,MONEY,RMB from t_role WHERE roleid = %s' % (str(role_id))
        pre_data = getdata(pre_select_sql)
        chage_pre_rmb = pre_data[0].get('RMB')

        add_diamonds_sql = 'update t_role set rmb=rmb+%s WHERE roleid=%s' %(int(add_diamonds), role_id)
        changedata(add_diamonds_sql)

        # 将修改的 rmb 值记录在 rmb_change_info 中
        chage_info_rw = rmb_change_info(uid=role_id, last_rmb=int(chage_pre_rmb), changed_rmb= int(add_diamonds))
        chage_info_rw.save()

        select_sql = 'SELECT ROLEID,ACCOUNTID,MONEY,RMB,`NAME`,FROM_UNIXTIME(LASTOFFLINETIME) as offtime from t_role WHERE roleid = %s'% (str(role_id))
        data = getdata(select_sql)
        # 数据类似： [{'NAME': '红枫叶', 'ROLEID': 1, 'RMB': 0, 'MONEY': 12500, 'ACCOUNTID': 1, 'FROM_UNIXTIME(LASTOFFLINETIME)': datetime.datetime(2018, 5, 25, 11, 30, 27)}]

        if len(data) < 1:
            print("don't get any data")
        elif len(data) == 1:
            data_dict = data[0] #取出 数据里面的字段
        else:
            print("get many data")
            print(data)
            data_dict = data[0]
        #print(data,data_dict.get('offtime'))
        html_data = {
            'disid': dis_uid,
            'roleid': role_id,
            'ACCOUNTID': data_dict.get('ACCOUNTID'),
            'disname': data_dict.get('NAME'),
            'dismoney': data_dict.get('MONEY'),
            'disrmb': data_dict.get('RMB'),
            'lastofftime': str(data_dict.get('offtime'))
        }

    return render(request,'diamonds/displayinfo.html', html_data)





