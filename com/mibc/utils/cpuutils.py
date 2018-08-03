#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/15 10:41
# @Author  : qingping.niu
# @File    : cpuutils.py
# @desc    : 获取CPU信息
from __future__ import division
from com.mibc.utils.log import logger,LOG
from decimal import Decimal

import subprocess,os

#
# class GetCpuUtils(object):
#     def test(self):
#         print()



    # initcpu = True
    #
    # global o_idle,o_cpu,c_idle,c_cpu
    # # o_idle = 0.0
    # # o_cpu = 0.0
    # #
    # # c_idle = 0.0
    # # c_cpu = 0.0
    #
    # @classmethod
    # def get_cpu_usage(self):
    #     global o_idle, o_cpu, c_idle, c_cpu
    #     if self.initcpu:
    #         print("--------------")
    #         self.initcpu = False
    #         try:
    #             cmd = 'adb shell cat /proc/stat'
    #             out_text = os.popen(cmd).readline()
    #             print(out_text)
    #             toks_list = out_text.split()
    #             o_idle = float(toks_list[4]) #从系统启动开始累积到当前时刻，除 IO 等待时间以外的其他等待时间。
    #             o_cpu = float(toks_list[1]) + \
    #                     float(toks_list[2]) + \
    #                     float(toks_list[3]) + \
    #                     float(toks_list[5]) + \
    #                     float(toks_list[6]) + \
    #                     float(toks_list[7])
    #             print(o_idle,o_cpu)
    #         except Exception as e:
    #             LOG('读取文件异常:%s' % e)
    #     else:
    #         try:
    #             print("***********")
    #             cmd = 'adb shell cat /proc/stat'
    #             out_text = os.popen(cmd).readline()
    #             out_text = os.popen(cmd).readline()
    #             toks_list = out_text.split()
    #             c_idle = float(toks_list[4])  # 从系统启动开始累积到当前时刻，除 IO 等待时间以外的其他等待时间。
    #             c_cpu = float(toks_list[1]) + \
    #                     float(toks_list[2]) + \
    #                     float(toks_list[3]) + \
    #                     float(toks_list[5]) + \
    #                     float(toks_list[6]) + \
    #                     float(toks_list[7])
    #             if (0 != ((c_cpu + c_idle) - (o_cpu + o_idle))):
    #                 usage = round((100.0 * (c_cpu - o_cpu) / ((c_cpu + c_idle) - (o_cpu + o_idle))),2)
    #                 print(usage)
    #
    #
    #
    #
    #
    #
    #
    #         except Exception as e:
    #             LOG('读取文件异常:%s' % e)
    #             pass








#
# if __name__ == '__main__':
#     for i in range(3):
#         GetCpuUtils.get_cpu_usage()



