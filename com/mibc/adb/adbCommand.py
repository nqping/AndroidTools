#!/usr/bin/sh python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/12 14:07
# @Author  : qingping.niu
# @File    : adbCommand.py
# @desc    : 获取各项性能数据命令集
import os
import subprocess,datetime,time
import uiautomator2 as u2

from com.mibc.utils.log import logger,LOG
from com.mibc.utils.systemstatus import getSystemStatus
from com.mibc.utils.devicesutils import getapp_architechture_type,getcpu_architecture_type,getdevices_list
from tkinter import messagebox

#获取系统环境状态
find = getSystemStatus()
devices = getdevices_list()


@logger('执行monkey测试')
def run_monkey(packagename,s_num,throttle,pct_touch,pct_motion,pct_trackball,pct_nav,pct_syskeys,pct_appswitch,num,logfilepath):
    cmdclear = 'adb logcat -c -b main -b events -b radio -b system'
    cmden='adb shell monkey -p %s -s %s --throttle %s --pct-touch %s --pct-motion %s  --pct-trackball  %s  --pct-trackball %s  --pct-syskeys  %s  --pct-appswitch  %s   -v -v -v %s >%s'%(packagename,s_num,throttle,pct_touch,pct_motion,pct_trackball,pct_nav,pct_syskeys,pct_appswitch,num,logfilepath)
    # LOG.info(cmden)
    #执行monkey前先清除所有缓存日志
    os.popen(cmdclear)
    os.popen(cmden)


@logger('获取启动耗时(root权限专用)')
def starttime_app(packagename,packagenameactivicy):#启动耗时
    cmd='adb shell am start -W -n %s'%packagenameactivicy
    # me=os.popen(cmd).read().split('\n')[-7].split(':')#获取启动时间
    me=os.popen(cmd).read().split("\n")[4].split(':')  #取Totaltime时间
    cmd2='adb shell am force-stop %s'%packagename
    os.system(cmd2)
    return me

@logger('获取设备状态')
def getDevicesStatus():#获取设备状态
    cmd1='adb get-state'
    devices_status=os.popen(cmd1).read().split()[0]
    return devices_status

@logger('获取内存信息')
def getMemory(packagename):
    try:
        cmd = 'adb shell dumpsys meminfo %s | %s TOTAL'%(packagename,find)
        LOG.info(cmd)
        output = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
        total=0
        if output.split() != "":
            total= output.split()[1]
        else:
            total = 0
        LOG.info(total)
        return total.decode()
    except:
        messagebox.showerror('错误','没有数据,请检查包名是否正确或等待几秒钟再执行一次')
        LOG.info('没有数据')



# @logger('获取cpu信息')
def getCpu(packagename):
    cmd = 'adb shell dumpsys cpuinfo | %s %s'%(find,packagename)
    LOG.info(cmd)
    # output = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
    output = subprocess.getoutput(cmd)
    if output.split() !="":
        cpu = output.split()[0]
        # LOG.info(cpu)
        return cpu.decode()

    # cmd = 'adb shell top -n 1 | %s %s'%(find,packagename)
    # output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
    # if output.split() != "":
    #     cpu = output.split()[index]
    #     print(cpu)
    #     return cpu.decode()

@logger('获取流量')
def getFlow(pacakgename):
    try:
        cmd = 'adb shell dumpsys package %s | %s userId'%(pacakgename,find)
        output = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
        temp =output.split()[0]
        pid = bytes.decode(temp).split('=')[1]
        LOG.info(pid)

        cmd1 = 'adb shell cat /proc/net/xt_qtaguid/stats | %s %s'%(find,pid)

        output1 = subprocess.Popen(cmd1,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
        rxBytes1_shou = output1.split()[5]  #接受[rx_bytes]
        txBytes1_xia = output1.split()[7]  #上传[tx_bytes] 传输

        cmd2 = 'adb shell cat /proc/net/xt_qtaguid/stats | %s %s'%(find,pid)
        output2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
        rxBytes2_shou = output2.split()[5]  # 接受[rx_bytes]
        txBytes2_xia = output2.split()[7]  # 上传[tx_bytes] 传输

        sum_shou = int(rxBytes1_shou) + int(rxBytes2_shou) #过程产生流量计算为执行后的流量-执行前的流量
        sum_xia = int(txBytes1_xia) + int(txBytes2_xia)
        sum = int(sum_xia) - int(sum_shou)

        flow_shan = int(txBytes1_xia) - int(rxBytes1_shou)
        flow_xia = int(txBytes2_xia) - int(rxBytes2_shou)
        # print("%s %s %s"%(flow_shan,flow_xia,sum))
        return flow_shan, flow_xia, sum
    except:
        messagebox.showerror('错误','网络读取异常')
        LOG.info('网络读取异常')

@logger('获取应用ROM占用大小')
def get_appsize(packagename):
    apksize = []
    loglist = []
    cmd='adb shell pm path %s'%packagename
    output = os.popen(cmd).readline()
    path = output.split(':')[1]
    cmd1 = 'adb shell du -h %s'%path

    output1 = os.popen(cmd1).readline()
    baseapk_size = output1.split()[0]
    apksize.append(baseapk_size)

    apkpath = path[0:path.rfind('/')]
    apkname = path[path.rfind('/')+1:path.rfind('.')]

    loglist.append(path)
    loglist.append(output1)

    arm_odex_path = '%s %s%s%s%s'%('adb shell du -h',apkpath,'/oat/arm/',apkname,'.odex')
    arm_vdex_path = '%s %s%s%s%s'%('adb shell du -h',apkpath,'/oat/arm/',apkname,'.vdex')
    arm64_odex_apth ='%s %s%s%s%s'%('adb shell du -h',apkpath,'/oat/arm64/',apkname,'.odex')
    arm64_vdex_path ='%s %s%s%s%s'%('adb shell du -h',apkpath,'/oat/arm64/',apkname,'.vdex')

    try:
        cpu_type = getcpu_architecture_type()
        app_type = getapp_architechture_type(packagename,cpu_type)

        if app_type == 32:
            arm_odex_rs = os.popen(arm_odex_path).read()
            arm_odex_size = arm_odex_rs.split()[0]
            apksize.append(arm_odex_size)
            loglist.append(arm_odex_rs)

            arm_vdex_rs = os.popen(arm_vdex_path).read()
            if 'du:' not in arm_vdex_rs and len(arm_vdex_rs) >0:
                arm_vdex_size = arm_vdex_rs.split()[0]
                apksize.append(arm_vdex_size)
                loglist.append(arm_vdex_rs)
        else:
            # print(arm64_odex_apth)
            arm64_odex_rs = os.popen(arm64_odex_apth).read()
            arm64_odex_size = arm64_odex_rs.split()[0]
            apksize.append(arm64_odex_size)
            loglist.append(arm64_odex_rs)
            arm64_vdex_rs = os.popen(arm64_vdex_path).read()
            # print(arm64_vdex_path)

            if 'du:' not in arm64_vdex_rs and len(arm64_vdex_rs) >0:
                arm64_vdex_size = arm64_vdex_rs.split()[0]
                print(arm64_vdex_size)
                apksize.append(arm64_vdex_size)
                loglist.append(arm64_vdex_rs)
    except:
        LOG.info('应用从未启动过,无法获取应用信息')
        messagebox.showerror('错误','应用从未启动过,获取信息不全')
        pass

    return loglist,apksize

@logger('获取应用运行时RAM占用大小')
def get_apprunram(cmd,packagename):
    '''获取应用运行时RAM占用大小,单位K'''
    output = subprocess.getoutput(cmd)
    ram_list = []
    # start = datetime.datetime.now()
    for line in output.split('\n'):
        if "Total PSS by OOM adjustment" in line:
            break;
        else:
            if packagename in line:
                LOG.info(line)
                ram_size = int(line.split(':')[0].split("K")[0].replace(",", "").strip())
                ram_list.append(ram_size)
    # end = datetime.datetime.now()
    # print(end - start)
    return ram_list

@logger('获取应用后台运行时RAM占用大小,场景1,2')
def get_appbackrunram(packagename,packageactivity,sleep_time):
    '''应用后台运行时RAM占用大小,单位K'''

    try:
        # 设备环境检查
        cmd = 'adb shell pm list packages | %s com.github.uiautomator ' % find
        output = subprocess.getstatusoutput(cmd)
        if output[0] != 0:
            LOG.info('uiautomator2环境未初始化')
            messagebox.showerror('错误','环境未初始化,请先执行python -m uiautomator2 init 初始化环境')

        else:

            devices = getdevices_list()
            LOG.info('设备%s'%devices)

            # 清空安装包缓存和数据
            cmdclear = 'adb shell pm clear %s' % packagename
            subprocess.getstatusoutput(cmdclear)
            # 连接并启动应用
            d = u2.connect(devices[0])
            d.app_start(packagename)
            messagebox.showinfo('提示', '应用已启动请手动操作进入首页')

            count = 0
            while count <=10:
                dict = d.current_app()
                if dict['activity'] in packageactivity:
                    break;
                count +=1
                time.sleep(30)

            LOG.info("已进入首页开始测试场景1")


            # cmdcheck = 'adb shell dumpsys activity activities | %s %s' % (find, packageactivity)
            #
            # count = 0
            # while count <= 10:
            #     output1 = subprocess.getstatusoutput(cmdcheck)
            #     if output1[0] == 0:
            #         break
            #     count += 1
            #     time.sleep(30)

            '''
                场景1
                1.进入应用首页后,按home退回后台
                2.打开系统设置页,修改Sleep时间为 Never
                3.按home退回后台,等待10分钟
                4.获取RAM值
                '''
            # 至应用于后台运行
            d.press('Home')
            # 打开系统setting页,并滑动页面找到最后一项(简单操作)
            d.app_start('com.android.settings')
            d(className='android.widget.FrameLayout').child_by_text(u"Display", allow_scroll_search=True,
                                                                    resourceId="android:id/title").click()
            d(className="android.widget.FrameLayout").child_by_text(u"Sleep", allow_scroll_search=True,
                                                                    resourceId="android:id/title").click()
            d(resourceId="com.android.settings:id/text1", text=u"Never").click()

            # 再切换到后台
            d.press('Home')
            time.sleep(sleep_time * 60)
            ram_list1 = get_apprunram('adb shell dumpsys meminfo', packagename)
            LOG.info('场景1结束--------------')

            '''
            场景2
            1.启动应用 按home退到后台
            2.进入系统设置修改Sleep时间为 30
            3.按home退回后台,等待10分钟
            4.获取RAM值
            '''
            d.app_start(packagename)
            time.sleep(3)
            # 至应用于后台运行
            d.press('Home')
            # 打开系统setting页,并滑动页面找到最后一项(简单操作)
            d.app_start('com.android.settings')
            d(className='android.widget.FrameLayout').child_by_text(u"Display", allow_scroll_search=True,
                                                                    resourceId="android:id/title").click()
            d(className="android.widget.FrameLayout").child_by_text(u"Sleep", allow_scroll_search=True,
                                                                    resourceId="android:id/title").click()
            d(resourceId="com.android.settings:id/text1", text=u"30 minutes").click()
            # 再切换到后台
            d.press('Home')
            time.sleep(sleep_time * 60)
            ram_list2 = get_apprunram('adb shell dumpsys meminfo', packagename)
            LOG.info('场景2结束--------------')

            return sum(ram_list1), sum(ram_list2)

    except Exception as e:
        LOG.info('场景1失败:%s'%e)
        messagebox.showerror('错误','测试失败原因%s'%e)





@logger('获取应用后台运行时RAM,场景3')
def get_appbackrunram2(packagename,sleep_time):
    '''
        场景3
        1.运行monkey命令
        2.monkey结束后按home键
        3.等待10分钟,查看RAM占用
    '''
    devices = getdevices_list()
    # 连接并启动应用
    d = u2.connect(devices[0])
    # 每隔一段时检测一次monkey进程
    d.press('Home')
    d.app_start('com.android.settings')
    d.press('Home')
    time.sleep(sleep_time * 60)
    ram_list3 = get_apprunram('adb shell dumpsys meminfo', packagename)
    LOG.info('场景3结束--------------')
    return sum(ram_list3)


def get_pid():
    cmd = 'adb shell ps -fe | %s monkey'%find
    output = subprocess.getstatusoutput(cmd)
    result = True if output[0]==0 else False
    LOG.info('monkey进程检查:%s'%result)
    return result

def uninstall_app(packagename,devices):
    cmd = 'adb -s %s uninstall %s'%(devices,packagename)
    output = subprocess.getoutput(cmd)
    return output





if __name__ == '__main__':
    out = subprocess.getoutput("adb uninstall com.tcl.adconfigdemo")
    print(out)

#     joutput = subprocess.
#     print(joutput)
    # find = getSystemStatus()
    # 获取系统环境状态
    # find = getSystemStatus()
    # getCpu('com.tct.calculator')
    # getMemory('com.tcl.live')
    # getFlow('com.tcl.live')
    # com.tct.calculator2
    # com.tct.calculator
    #com.tcl.joylockscreen
    #com.tcl.live
    # loglist,apksize = get_appsize('com.tcl.joylockscreen')
    # print(loglist)
    # print(apksize)
    # get_apprunram("adb shell dumpsys meminfo","com.tcl.live")

    # list = get_apprunram("adb shell dumpsys meminfo", "com.tcl.joylockscreen")
    # print(list)


    # get_appsize('com.tct.calculator')
