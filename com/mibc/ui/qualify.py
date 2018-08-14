#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 17:52
# @Author  : qingping.niu
# @File    : qualify.py
# @desc    : Qualify 测试报告相关内容
import tkinter as tk
import threading,datetime,time,subprocess
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from com.mibc.utils.log import logger,LOG
from com.mibc.adb.adbCommand import get_appromsize,get_pid,get_appramruning

class Qualify(object):
    def __init__(self, **kwargs):
        mainFram = kwargs.get('mainFram')
        self.packname = kwargs.get('pckname')
        self.devices = kwargs.get('devices')

        pwindow = PanedWindow(mainFram, orient=VERTICAL, showhandle=False, sashrelief=SUNKEN)  # 默认是左右分布的
        pwindow.pack(fill=BOTH, expand=1)

        self.frame_top = Frame(mainFram, height=300, width=800)
        self.frame_top.propagate(0)  # 0表示父窗口依以子控件大小调整
        self.frame_top.pack(fill=BOTH, expand=1)

        self.frame_bottom = Frame(mainFram)
        self.frame_bottom.pack(fill=BOTH, expand=1)

        self.data_text = ScrolledText(self.frame_bottom)
        self.data_text.pack(fill=BOTH, expand=1)

        pwindow.add(self.frame_top)
        pwindow.add(self.frame_bottom)

        # self.create_appromsize_widget()


    def create_appromsize_widget(self):
        '''创建 应用ROM 大小控件'''
        self.appsize_lf = ttk.LabelFrame(self.frame_top,text='应用ROM',width=800,height=400)
        self.appsize_lf.pack(fill=BOTH,expand=1)

        ttk.Label(self.appsize_lf,text='包名:').grid(row=0,column=1,pady=10)
        self.appsize_pck= ttk.Entry(self.appsize_lf,width=45,state='readonly',textvariable= self.packname)
        self.appsize_pck.grid(row=0,column=2)

        start_btn = ttk.Button(self.appsize_lf, text='开始测试',command=self.thread_appromsize)
        start_btn.grid(row=2,column=2)

    def create_appruning_widget(self):
        '''创建应用运行时RAM'''
        self.apprun_lf = ttk.LabelFrame(self.frame_top, text='应用运行时RAM', width=800,height=300)
        self.apprun_lf.pack(fill=BOTH, expand=1)

        Label(self.apprun_lf, text='包名:').grid(row=0, column=1, pady=10, sticky=E)
        self.pckname_appram = ttk.Entry(self.apprun_lf,width=30,textvariable=self.packname, state='readonly')
        self.pckname_appram.grid(row=0,column=2,sticky=W)


        Label(self.apprun_lf, text='监控间隔时间(分):').grid(row=1, column=1, pady=10, sticky=E)
        num = [2, 4, 6, 8, 10, 15]
        self.monitoring_time = ttk.Combobox(self.apprun_lf, values=num, state='readonly', width=10)
        self.monitoring_time.current(0)
        self.monitoring_time.grid(row=1, column=2, sticky=W)

        Label(self.apprun_lf, text='监控命令:').grid(row=2, column=1, pady=10, sticky=E)
        self.runcommand = Text(self.apprun_lf, height=3, width=80)
        self.runcommand.insert(END, 'adb shell dumpsys meminfo')
        self.runcommand.grid(row=2, column=2, sticky=W)

        Label(self.apprun_lf, text='monkey命令:').grid(row=3, column=1)
        self.monkeycommand = Text(self.apprun_lf, height=4, width=80)
        self.monkeycommand.insert(END,
                                  'adb shell monkey -p 包名 -s 10 --pct-touch 30 --throttle 300 -v 10000 --monitor-native-crashes')
        self.monkeycommand.grid(row=3, column=2, pady=10)

        btn_start = ttk.Button(self.apprun_lf, text='开始测试', command=self.thread_appram_runing)
        btn_start.grid(row=4, column=2)

    def thread_appram_runing(self):
        for i in range(1):
            t = threading.Thread(target=self.getappramruning, args=())
            t.start()

    def thread_appromsize(self):
        for i in range(1):
            t = threading.Thread(target=self.getappromsize, args=())
            t.start()

    def getappramruning(self):
        '''获取应用运行时RAM占用大小'''
        devcies = self.devices.get()
        packagename = self.pckname_appram.get().strip()
        runcommand = self.runcommand.get('0.0', END).strip()  # 监控命令
        monkeycommand = self.monkeycommand.get('0.0', END).strip()  # monkey命令
        sleep_time = int(self.monitoring_time.get())  # 监控间隔时间

        if len(packagename) <= 5 or len(runcommand) <= 5 or len(monkeycommand) <= 5:
            messagebox.showwarning('警告', '请检查参数')
        else:
            count_list = []  # 次数
            max_list = []

            # 运行monkey命令
            subprocess.Popen(monkeycommand)
            time.sleep(2)
            i = 0
            while get_pid(devcies,'monkey'):
                current_time = datetime.datetime.now().strftime('%H:%M:%S')
                ram_list = get_appramruning(runcommand, packagename)
                ram_sum = sum(ram_list)
                max_list.append(ram_sum)
                i += 1
                count_list.append(i)
                text = '%s 第%s次 %sK \n' % (current_time, i, ram_sum)
                self.data_text.insert(END, text)
                self.data_text.see(END)
                time.sleep(sleep_time * 60)

            _max = round(max(max_list) / 1024, 2)
            print(max(max_list) / 1024)
            text1 = '最大值:%sK / 1024 = %sM' % (max(max_list), _max)
            self.data_text.insert(END, text1)
            self.data_text.update()
            messagebox.showinfo('提醒', '测试完成')

    def getappromsize(self):
        '''获取应用ROM占用大小'''
        devices = self.devices.get()
        if len(devices) > 0:
            packagename = self.appsize_pck.get()
            if len(packagename) <= 5:
                LOG.info('包名必须真实有效')
                messagebox.showwarning('警告', '请检查您的包名')
            else:
                rslist, apkromsize = get_appromsize(packagename, devices)
                print(rslist)
                for i in rslist:
                    self.data_text.insert(END, i)
                    self.data_text.insert(END, '\n')
        else:
            LOG.info('测试的设备必须正常连接，请注意')
            messagebox.showwarning('警告', '设备连接异常 请重新连接设备!')

