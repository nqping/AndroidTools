#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/14 17:10
# @Author  : qingping.niu
# @File    : dataUtils.py
# @desc    :

import datetime

#两个时间对比
def contrast(data1,data2):
    datatime1 = datetime.datetime.strftime(data1,'%Y-%m-%d %H:%M:%S')
    datatime2 = datetime.datetime.strftime(data2,'%Y-%m-%d %H:%M:%S')
    if datatime1 <= datatime2:
        return True
    else:
        return False

def getHour():
    hour = datetime.datetime.now().strftime('%H:%M:%S')
    print(hour)


# if __name__=='__main__':
#     current_time = datetime.datetime.now().strftime('%H:%M:%S')
#     print(current_time)



