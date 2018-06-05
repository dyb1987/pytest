import pymysql
import datetime
import time

def produce_sql_func(back_data_db, back_data_table, old_data_db, old_data_table, where_colum, del_time):
    back_sql = 'insert into %s.%s SELECT * from %s.%s WHERE %s < "%s"' % (back_data_db, back_data_table, old_data_db,
                                                                          old_data_table, where_colum, str(del_time))

    del_data_sql = 'delete from %s.%s WHERE %s < "%s"' % (old_data_db, old_data_table, where_colum, str(del_time))
    return (back_sql, del_data_sql)


def main_fun(backsql, delsql):
    gamedb_yyde = {
        'host': '192.168.1.150',
        'user': 'root',
        'password': 'cqmfindbpwd',
        'db': '',
        'port': 33306,
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
    }

    # 创建连接 接受字典的 参数
    db_yyde_connected = pymysql.connect(**gamedb_yyde)

    # 创建游标
    yyde_cur = db_yyde_connected.cursor()

    yyde_sql = backsql

    # 执行SQL
    #yyde_cur.execute(yyde_sql)
    # data = yyde_cur.fetchone()
    #yydedb_data = yyde_cur.fetchmany(size=10)
    # 下面这种插入方式有问题
    # 每天记录是一个字典，类似
    # 获取插入 表里的 字段名 和 字段的值
    # for data_item in yydedb_data
    # list(data_item) --> ['GOODSTYPE', 'GOLD', 'ACTION', 'ROLEID', 'TIME', 'TOKEN', 'GOODSNUM', 'ID']
    # list(data_item.values()) --> [23, 10001, '23消耗元宝', 167045, datetime.datetime(2018, 5, 3, 0, 0, 3), 30, 1, 501570]
    print(yyde_sql)
    print(delsql)
    try:
        yyde_cur.execute(yyde_sql)
        time.sleep(2)
        yyde_cur.execute(delsql)
        db_yyde_connected.commit()
    except Exception as e:
        print(e)
    else:
        pass
    finally:
        yyde_cur.close()
        db_yyde_connected.close()



if __name__ == "__main__":
    now_date = datetime.datetime.today()
    many_days_ago = now_date - datetime.timedelta(days=6)

    # 合并时间格式，最后格式 类似 2018-05-22 00:00:00
    delte_date_time = datetime.datetime.combine(many_days_ago, datetime.time(00, 00, 00))
    # print(str(delte_date_time))
    (backsql, delsql) = produce_sql_func('test', 't_consume', 'gamedb_xsbh', 't_consume', 'TIME', del_time=str(delte_date_time))
    main_fun(backsql,delsql)

    # t_roomrecord
    (backsql, delsql) = produce_sql_func('test', 't_roomrecord', 'gamedb_xsbh', 't_roomrecord', 'ENDTIME',del_time=str(delte_date_time))
    main_fun(backsql, delsql)






