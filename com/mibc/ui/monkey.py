#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/8 11:09
# @Author  : qingping.niu
# @File    : monkey.py
# @desc    : Monkey测试

import tkinter as tk
import threading,time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from com.mibc.utils.log import logger,LOG
from com.mibc.adb.adbCommand import run_monkey,kill_process,get_pid
from com.application import Application


class Monkey(object):
    def __init__(self,**kwargs):
        mainFram = kwargs.get('mainFram')


        self.packname = kwargs.get('pckname')
        self.devices = kwargs.get('devices')

        pwindow = PanedWindow(mainFram, orient=VERTICAL, showhandle=False, sashrelief=SUNKEN)  # 默认是左右分布的
        pwindow.pack(fill=BOTH, expand=1)

        self.frame_top = Frame(mainFram,height=400,width=800)
        self.frame_top.propagate(0)  # 0表示父窗口依以子控件大小调整
        self.frame_top.pack(fill=BOTH, expand=1)

        self.frame_bottom = Frame(mainFram)
        self.frame_bottom.pack(fill=BOTH, expand=1)

        pwindow.add(self.frame_top)
        # pwindow.add(self.frame_bottom)
        self.create_monkey_widget()



    def create_monkey_widget(self):
        """定义monkey控件"""
        # 定义变量
        self.filevar = tk.StringVar()

        self.monkey_lafr = ttk.LabelFrame(self.frame_top, text='Monkey测试',width=800,height=400)
        # self.monkey_lafr.pack_propagate(1)
        self.monkey_lafr.pack(fill=BOTH, expand=1)

        Label(self.monkey_lafr, text='触摸事件:--pct-touch').grid(row=1, column=1, sticky=E)
        self.pcttouch = ttk.Entry(self.monkey_lafr, width=30)
        self.pcttouch.grid(row=1, column=2, sticky=W, pady=5)
        self.pcttouch.insert(0, 10)

        Label(self.monkey_lafr, text='动作事件:--pct-motion').grid(row=1, column=3, sticky=E)
        self.pctmotion = ttk.Entry(self.monkey_lafr, width=30)
        self.pctmotion.grid(row=1, column=4, sticky=W, pady=5)
        self.pctmotion.insert(0, 10)

        Label(self.monkey_lafr, text='轨迹事件:--pct-trackball').grid(row=2, column=1, sticky=E)
        self.pcttrackball = ttk.Entry(self.monkey_lafr, width=30)
        self.pcttrackball.grid(row=2, column=2, sticky=W, pady=5)
        self.pcttrackball.insert(0, 10)

        Label(self.monkey_lafr, text='系统事件:--pct-syskeys').grid(row=2, column=3, sticky=E)
        self.pctsyskeys = ttk.Entry(self.monkey_lafr, width=30)
        self.pctsyskeys.grid(row=2, column=4, sticky=W, pady=5)
        self.pctsyskeys.insert(0, 10)

        Label(self.monkey_lafr, text='基本导航:--pct-nav').grid(row=3, column=1, sticky=E)
        self.pctnav = ttk.Entry(self.monkey_lafr, width=30)
        self.pctnav.grid(row=3, column=2)
        self.pctnav.insert(0, 10)

        Label(self.monkey_lafr, text='主要导航:--pct-majornav').grid(row=3, column=3, sticky=E)
        self.pctmajornav = ttk.Entry(self.monkey_lafr, width=30)
        self.pctmajornav.grid(row=3, column=4, sticky=W, pady=5)
        self.pctmajornav.insert(0, 10)

        Label(self.monkey_lafr, text='切屏事件:--pct-appswitch').grid(row=4, column=1, sticky=E)
        self.pctappswitch = ttk.Entry(self.monkey_lafr, width=30)
        self.pctappswitch.grid(row=4, column=2, sticky=W, pady=5)
        self.pctappswitch.insert(0, 10)

        Label(self.monkey_lafr, text='点击事件:--pct-flip').grid(row=4, column=3, sticky=E)
        self.pctflip = ttk.Entry(self.monkey_lafr, width=30)
        self.pctflip.grid(row=4, column=4, sticky=W, pady=5)
        self.pctflip.insert(END, 20)

        Label(self.monkey_lafr, text='其它事件:--pct-anyevent').grid(row=5, column=1, sticky=E)
        self.pctanyevent = ttk.Entry(self.monkey_lafr, width=30)
        self.pctanyevent.grid(row=5, column=2, sticky=W, pady=5)
        self.pctanyevent.insert(END, 10)

        Label(self.monkey_lafr, text='延迟时间:--throttle').grid(row=5, column=3, sticky=E)
        self.throttle = ttk.Entry(self.monkey_lafr, width=30)
        self.throttle.grid(row=5, column=4, sticky=W, pady=5)
        self.throttle.insert(0, 500)

        Label(self.monkey_lafr, text='事件数量:').grid(row=6, column=1, sticky=E)
        self.event_num = ttk.Entry(self.monkey_lafr, width=30)
        self.event_num.grid(row=6, column=2, sticky=W, pady=5)
        self.event_num.insert(0, 10000)


        ttk.Label(self.monkey_lafr, text='伪随机数:-s<seed>').grid(row=6, column=3, sticky=E)
        self.event_t = ttk.Entry(self.monkey_lafr, width=30)
        self.event_t.grid(row=6, column=4, sticky=W, pady=5)
        self.event_t.insert(0,1000)

        Label(self.monkey_lafr, text='日志级别:').grid(row=7, column=1, sticky=E)
        loglevel = ['-v -v -v','-v -v','-v']
        self.loglevel_c = ttk.Combobox(self.monkey_lafr, values=loglevel)
        self.loglevel_c.current(0)
        self.loglevel_c.grid(row=7, column=2, sticky=W, pady=5)


        Label(self.monkey_lafr, text='包名:').grid(row=7, column=3, sticky=E)
        self.package_t1 = ttk.Entry(self.monkey_lafr, width=30, textvariable=self.packname, state='readonly')
        self.package_t1.grid(row=7, column=4, sticky=W, pady=5)

        Label(self.monkey_lafr, text='日志路径:').grid(row=8, column=1, sticky=E)
        self.log_path = ttk.Entry(self.monkey_lafr, width=30, textvariable=self.filevar,state='readonly')
        self.log_path.grid(row=8, column=2, sticky=W, pady=5)
        self.log_path.bind('<ButtonPress-1>', self.__opendir)


        btn_monkey = ttk.Button(self.monkey_lafr, text='开始测试', command=self.thread_start_monkey)
        btn_monkey.grid(row=8, column=3, sticky=E, pady=10)

        stop_monkey_btn = ttk.Button(self.monkey_lafr, text='结束测试',command=self.thread_stop_monkey)
        stop_monkey_btn.grid(row=8, column=4, sticky=E, pady=10)


    def __opendir(self,*args):
        '''打开目录对话框'''
        dirname = filedialog.askdirectory()  # 打开文件夹对话框
        self.filevar.set(dirname)

    def thread_stop_monkey(self):
        for i in range(1):
            t = threading.Thread(target=self.stop_monkey, args=())
            t.start()
    def thread_start_monkey(self):
        for i in range(1):
            t = threading.Thread(target=self.monkey_app,args=())
            t.start()

    def stop_monkey(self):
        '''结束monkey'''
        try:
            devices = self.devices.get()
            # 先结束monkey进程
            monkey_pid = get_pid(devices, 'monkey')
            kill_process(devices,monkey_pid)

            #再结束logcat进程
            logcat_pid = get_pid(devices, 'logcat')
            kill_process(devices,logcat_pid)
            messagebox.showinfo('提示','结束测试成功')

        except:
            LOG.info('结束monkey进程失败')
            messagebox.showerror('错误','进程结束失败')



    def monkey_app(self):
        devices = self.devices.get()
        if len(devices) > 0:
            try:
                packname = self.package_t1.get().strip()
                logpath = self.log_path.get().strip()
                loglevel = self.loglevel_c.get()
                event = self.event_t.get().strip() #伪随机数 -s<seed>
                throttle = self.throttle.get().strip()
                eventnum = self.event_num.get().strip()

                pcttouch = int(self.pcttouch.get().strip())
                pctmotion = int(self.pctmotion.get().strip())
                pcttrackball = int(self.pcttrackball.get().strip())
                pctsyskeys = int(self.pctsyskeys.get().strip())
                pctnav = int(self.pctnav.get().strip())
                pctmajornav = int(self.pctmajornav.get().strip())
                pctappswitch = int(self.pctappswitch.get().strip())
                pctflip = int(self.pctflip.get().strip())
                pctanyevent = int(self.pctanyevent.get().strip())

                sum = pcttouch + pctmotion + pcttrackball + pctsyskeys + pctnav + pctmajornav + pctappswitch + pctflip + pctanyevent

                if len(packname) <= 5:
                    LOG.info('请正确填写包名')
                    messagebox.showwarning('提醒', '请正确填写包名')
                elif sum >100:
                    messagebox.showerror('提醒', '您输入的所有的事件的比例和不能超过100%')
                    LOG.info('您输入的所有的事件的比例和不能超过100')
                else:

                    run_monkey(devices=devices, packagename=packname, pcttouch=pcttouch, pctmotion=pctmotion, pcttrackball=pcttrackball,
                               pctsyskeys=pctsyskeys, pctnav=pctnav, pctmajornav=pctmajornav, pctappswitch=pctappswitch, pctflip=pctflip,
                               pctanyevent=pctanyevent, event=event,
                               throttle=throttle, loglevel=loglevel, eventnum=eventnum, logpath=logpath)

                    while get_pid(devices,'monkey'):
                        time.sleep(60)

                    logcat_pid = get_pid(devices,'logcat')
                    kill_process(devices,logcat_pid)



            except:
                messagebox.showwarning('警告', '必须填写monkey相关数据')
                LOG.info('monkey 测试出错，原因:%s' % Exception)
        else:
            LOG.info('设备连接异常 请重新连接设备!')
            messagebox.showwarning('警告', '设备连接异常 请重新连接设备!')





