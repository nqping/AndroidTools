#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/15 15:44
# @Author  : qingping.niu
# @File    : devicesutils.py
# @desc    : 获取设备信息

from com.mibc.utils.log import logger,LOG
import subprocess,os
from tkinter import messagebox
from com.mibc.utils.systemstatus import getSystemStatus

ANDROID_VERSION_CMD = 'adb shell getprop ro.build.version.release'
ANDROID_VERSION_SDK_CMD = 'adb shell getprop ro.build.version.sdk'
ANDROID_DISPLAY_SIZE_CMD = 'adb shell wm size'
CPU_ARCHITECTURE_TYPE_32 = 32
CPU_ARCHITECTURE_TYPE_64 = 64

APP_ARCHITECTURE_TYPE_32 = 32
APP_ARCHITECTURE_TYPE_64 = 64
#获取系统环境状态
find = getSystemStatus()



@logger('获取多个设备')
def getdevices_list():
    devices = []
    result = os.popen("adb devices").readlines()
    result.reverse()  # 内容反转
    try:
        for line in result:
            li = line.strip()
            if not len(li) or "attached" in li or "?" in li or "offline" in li:
                continue
            else:
                devices.append(li.split()[0])

        LOG.info(devices)
        return devices
    except Exception as e:
        LOG.error('Failed to get devices:%s'%e)



@logger('获取android版本,sdk版本,分辨率,型号,名称,品牌,产商')
def getdevices_info():
    devices_dict = {}
    cmd = 'adb shell getprop | %s product' % find
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
    version = os.popen(ANDROID_VERSION_CMD).read()
    sdk_version = os.popen(ANDROID_VERSION_SDK_CMD).read()
    display_size = os.popen(ANDROID_DISPLAY_SIZE_CMD).read().split(":")[1]

    devices_dict.setdefault("version", version.strip())
    devices_dict.setdefault("display_size", display_size.strip())
    devices_dict.setdefault("sdk_version", sdk_version.strip())

    for lie in result.readlines():
        li = lie.strip().decode()

        if "ro.product.model" in li:
            model = li.split(":")[1][2:-1]
            devices_dict.setdefault("model", model)  # 型号
        elif "ro.product.brand" in li:
            brand = li.split(":")[1][2:-1]
            devices_dict.setdefault("brand", brand)  # 品牌
        elif "ro.product.device" in li:
            device = li.split(":")[1][2:-1]
            devices_dict.setdefault("device", device)  # 名称
        elif "ro.product.manufacturer" in li:
            manufacturer = li.split(":")[1][2:-1]
            devices_dict.setdefault("manufacturer", manufacturer)  # 产商

    return devices_dict

@logger('获取android版本')
def getandroid_version():
    version = os.popen(ANDROID_VERSION_CMD).read()
    if version.strip() == "":
        return None
    else:
        return int(version[:1])

@logger('获取设备状态')
def getDevicesStatus():#获取设备状态
    try:
        cmd1 = 'adb get-state'
        devices_status = os.popen(cmd1).read().split()[0]
        return devices_status
    except:
        # LOG.info('获取设备状态异常')
        messagebox.showwarning('警告','请检查设备状态')

def getcpu_architecture_type():
    '''获取CPU 位数 32 or 64'''
    cmd='adb shell ps | %s zygote64'%find
    rslines = os.popen(cmd).read()
    if 'zygote64' not in rslines:
        return CPU_ARCHITECTURE_TYPE_32
    return CPU_ARCHITECTURE_TYPE_64

def getapp_architechture_type(packagename,cputype):
    '''获取32or64位的APP'''
    if cputype == 32:
        cmd = 'adb shell ps | %s zygote' %find
        pid = os.popen(cmd).readline().split()[1]
        cmd1 ='adb shell ps | %s %s'%(find,pid)
        output = os.popen(cmd1).readlines()
        for lin in output:
            if packagename in lin:
                return APP_ARCHITECTURE_TYPE_32
    else:
        cmd64_1 = 'adb shell ps | %s zygote64' % find
        pid64 = os.popen(cmd64_1).readline().split()[1]
        cmd64_2 = 'adb shell ps | %s %s' % (find, pid64)
        output_64 = os.popen(cmd64_2).readlines()
        for lin in output_64:
            if packagename in lin:
                return APP_ARCHITECTURE_TYPE_64


def getcpu_top_index():
    version = getandroid_version()
    if version == 4 or version == 5 or version == 6:
        return 2;
    elif version == 7:
        return 4
    else:
        return 8

#
# if __name__=='__main__':
#     devices = getdevices_list()
#     print(devices[0])
    # 获取系统环境状态
    # find = getSystemStatus()
    # cputype = getapp_architechture_type('com.tcl.live',64)
    # # cputype = getcpu_architecture_type()
    # print(cputype)
    # print(len('adb shell dumpsys activity activities | findstr[grep] mFocusedActivity (适用8.0及以上)'))
