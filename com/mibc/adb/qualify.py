#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/24 10:56
# @Author  : qingping.niu
# @File    : qualify.py
# @desc    :
from com.mibc.utils.systemstatus import getSystemStatus
from com.mibc.utils.devicesutils import getdevices_list
import uiautomator2 as u2

#获取系统环境状态
# find = getSystemStatus()
#
# class Qualify(object):
#
#     def __init__(self):
#         self.devices = getdevices_list()
#
#
#
#     @classmethod
#     def get_memroy(self):
#         print()