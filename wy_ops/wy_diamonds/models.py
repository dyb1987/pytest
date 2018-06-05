from django.db import models
import datetime
# django admin 用户为: testpwd,
# djang admin 为 adminpwd123,

# Create your models here.
# 修改日志结构：
# 表名：rmb_change_info
# 自增ID： 默认 django 会为你创建
# 修改的UID：uid
# 修改前的值: last_rmb
# 修改后的值：changed_rmb
# 修改时间：change_time

class rmb_change_info(models.Model):
    uid = models.IntegerField(null=False)
    last_mondey = models.IntegerField(default=0, null=False)
    changed_money = models.IntegerField(default=0, null=False)
    last_rmb = models.IntegerField(default=0, null=False)
    changed_rmb = models.IntegerField(default=0, null=False)
    changed_time = models.DateTimeField(auto_now=True)


