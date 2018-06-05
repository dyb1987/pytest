import datetime
print(datetime.datetime.now())

li = [{'NAME': '红枫叶', 'ROLEID': 1, 'RMB': 0, 'MONEY': 12500, 'ACCOUNTID': 1, 'FROM_UNIXTIME(LASTOFFLINETIME)': datetime.datetime(2018, 5, 25, 11, 30, 27)}]

li_temp=li[0].get('MONEY')
li_temp2=li[0].get('NAME')
print(li_temp,li_temp2)