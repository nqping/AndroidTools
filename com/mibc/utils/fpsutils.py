#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/21 17:15
# @Author  : qingping.niu
# @File    : fpsutils.py
# @desc    :

import os,subprocess

def get_fps_activity(activity):
    cmd ='adb shell dumpsys activity|findstr mFocusedActivity'

    out_put = subprocess.getoutput(cmd)
    package_activity = out_put.replace("{","").replace("}","").split()[3]
    if package_activity == activity :
        cmd = 'adb shell dumpsys SurfaceFlinger --latency %s' %package_activity
        print(cmd)
        out_put_t = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE).stdout.readlines()
        print(out_put_t)





# if __name__=='__main__':
#     get_fps_activity('com.tcl.joylockscreen/.settings.activity.SettingsMainActivity')