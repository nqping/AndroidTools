#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/20 12:24
# @Author  : qingping.niu
# @File    : application.py
# @desc    : 主界面
import tkinter as tk
import threading,datetime,time
import base64
from com.image.icon import img
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from com.mibc.utils.devicesutils import getDevicesStatus,getdevices_info,getdevices_list
from com.mibc.adb.adbCommand import *
from com.mibc.utils.dataUtils import contrast
from com.mibc.utils.log import logger,LOG
from com.mibc.utils.py_excel import saveStartAppResult,saveCpuResult


class Application(tk.Tk):
    global packagename

    def __init__(self,devices):
        '''初始化'''
        super().__init__()  # 有点相当于tk.Tk()
        self.__running = True
        self.devices_list = devices

        # 获取设备状态
        # self.devices_status = getDevicesStatus()
        # self.devices_list = getdevices_list()


        self.create_panel_frame()
        self.__create_cpu_widget()
        self.__create_menu_widget()


        # self.__create_monkey_widget()

    def create_panel_frame(self):
        '''布局'''
        self.entryvar = tk.StringVar() #变量
        framebar = tk.Frame(self,height=80)
        framebar.pack(side=TOP)

        contentframe = Frame(self)
        contentframe.pack(side=TOP,fill=BOTH,expand=1)

        pwindow = PanedWindow(contentframe,orient=VERTICAL, showhandle=False, sashrelief=SUNKEN)  # 默认是左右分布的
        pwindow.pack(fill=BOTH, expand=1)

        self.frame_top = Frame(pwindow,height=250,width=800)
        self.frame_top.propagate(0) #0表示父窗口依以子控件大小调整
        self.frame_top.pack(fill=BOTH, expand=1)

        self.frame_bottom = Frame(pwindow)
        self.frame_bottom.pack(fill=BOTH, expand=1)

        self.glabel_l = tk.Label(framebar, text='说明:')
        self.glabel_l.grid(row=0,column=1,sticky=E)

        tk.Label(framebar, text='全局包名:').grid(row=1,column=1)
        self.global_package = tk.Entry(framebar,width=30,textvariable=self.entryvar)
        self.global_package.grid(row=1, column=2,sticky=W)

        tk.Label(framebar, text='设备:').grid(row=1,column=3)

        self.devcies_combobox = ttk.Combobox(framebar, values=self.devices_list)
        self.devcies_combobox.current(0)
        self.devcies_combobox.grid(row=1, column=4, sticky=W)

        self.data_text = ScrolledText(self.frame_bottom)
        self.data_text.pack(fill=BOTH, expand=1)


        # self.data_text = Scrollbar(textPad)  # 右侧的移动下滑栏
        # textPad.config(yscrollcommand=scroll.set)  # 在Y轴显示   yscrollcommand
        # scroll.config(command=textPad.yview)  # 这是为了让编辑内容和下拉栏同时移动
        # scroll.pack(side=RIGHT, fill=Y)  # 显示


        pwindow.add(self.frame_top)
        pwindow.add(self.frame_bottom)


    def __create_cpu_widget(self):
        '''创建cpu控件'''

        self.lable_f = LabelFrame(self.frame_top,text="性能测试",padx=10, pady=10)
        self.lable_f.pack(fill=BOTH,expand=1)

        # Label(self.lable_f,text='包名:').grid(row=0,column=1)
        # self.global_package = Entry(self.lable_f,width=50)
        # self.global_package.grid(row=0,column=2)

        Label(self.lable_f, text='间隔时间(s):').grid(row=1, column=1, padx=10,pady=10)
        intervaTime_ev = [3, 5, 10, 15]  # 这里还原可以增加可以选择的次数
        self.intervatime_t = ttk.Combobox(self.lable_f, values=intervaTime_ev)
        self.intervatime_t.current(0)
        self.intervatime_t.grid(row=1, column=2, sticky=W)

        Label(self.lable_f, text='持续时间(分):').grid(row=3, column=1, padx=10)
        chixuntime_ev = [5, 10, 20, 30, 60]  # 持续执行时间以分钟为单位
        self.chixuntime_t = ttk.Combobox(self.lable_f, values=chixuntime_ev)
        self.chixuntime_t.current(0)
        self.chixuntime_t.grid(row=3, column=2, sticky=W)

        self.cpu_btn_start = Button(self.lable_f, text='开始测试', command=self.thread_cpu_app_test )
        self.cpu_btn_start.grid(row=4, column=1, sticky=E,pady=10)

        self.cpu_btn_stop = Button(self.lable_f, text='强制结束', command=self.thread_stop, state='disabled')
        self.cpu_btn_stop.grid(row=4, column=2, sticky=E)


    def __create_monkey_widget(self):
        '''创建monkey控件'''
        self.monkey_lafr = LabelFrame(self.frame_top,text="Monkey测试")
        self.monkey_lafr.pack(fill=BOTH,expand=1)

        Label(self.monkey_lafr, text='伪随机数:').grid(row=0, column=1)
        self.event_t = Text(self.monkey_lafr, height=1, width=30)
        self.event_t.insert('0.0', 0)
        self.event_t.grid(row=0, column=2)

        Label(self.monkey_lafr, text='随机种子个').grid(row=0, column=3)
        self.zhongzi_t = Text(self.monkey_lafr, height=1, width=30)
        self.zhongzi_t.grid(row=0, column=4)

        Label(self.monkey_lafr, text='导航事件百分比：').grid(row=1, column=1)
        self.danghang_t = Text(self.monkey_lafr, height=1, width=30)
        self.danghang_t.insert('0.0', 0)
        self.danghang_t.grid(row=1, column=2)
        Label(self.monkey_lafr, text='触摸事件百分比：').grid(row=1, column=3)
        self.touch_t = Text(self.monkey_lafr, height=1, width=30)
        self.touch_t.grid(row=1, column=4)
        self.touch_t.insert('0.0', 0)

        Label(self.monkey_lafr, text='滑动事件百分比：').grid(row=2, column=1)
        self.huadong_t = Text(self.monkey_lafr, height=1, width=30)
        self.huadong_t.grid(row=2, column=2)
        self.huadong_t.insert('0.0', 0)
        Label(self.monkey_lafr, text='轨迹球事件百分比:').grid(row=2, column=3)
        self.trackball_t = Text(self.monkey_lafr, height=1, width=30)
        self.trackball_t.grid(row=2, column=4)
        self.trackball_t.insert('0.0', 0)

        Label(self.monkey_lafr, text='系统按键百分比：').grid(row=3, column=1)
        self.xitong_t = Text(self.monkey_lafr, height=1, width=30)
        self.xitong_t.grid(row=3, column=2)
        self.xitong_t.insert('0.0', 0)
        Label(self.monkey_lafr, text='activity之间的切换百分比:').grid(row=3, column=3)
        self.acti_t = Text(self.monkey_lafr, height=1, width=30)
        self.acti_t.grid(row=3, column=4)
        self.acti_t.insert('0.0', 0)

        Label(self.monkey_lafr, text='时间间隔：').grid(row=4, column=1)
        suji_event = [100, 500, 1000, 1500, 2000, 3000]
        self.time_t = ttk.Combobox(self.monkey_lafr, values=suji_event)
        self.time_t.current(0)
        self.time_t.grid(row=4, column=2,sticky=W)

        Label(self.monkey_lafr, text='日志存放路径:').grid(row=4, column=3)
        self.log_t = Text(self.monkey_lafr, height=1, width=30)
        self.log_t.grid(row=4, column=4)
        self.log_t.insert('0.0', 'F:\\monekey.txt')

        Label(self.monkey_lafr, text='包名:').grid(row=5,column=1)
        self.package_t1 = Text(self.monkey_lafr,height=1,width=30)
        self.package_t1.grid(row=5,column=2,sticky=W)

        btn_monkey = Button(self.monkey_lafr, text='开始测试', command=self.monkey_app)
        btn_monkey.grid(row=5, column=3,sticky=E,pady=10)


    def __create_devices_widget(self):
        '''设备信息控件'''

        devices_dict = getdevices_info()

        self.info_lafr = LabelFrame(self.frame_top, text="设备信息",padx=10, pady=10)
        Label(self.info_lafr, text='名称:').grid(row=0, column=1)
        Label(self.info_lafr, text=devices_dict['device'],width=30).grid(row=0, column=2)

        Label(self.info_lafr, text='型号:').grid(row=0, column=3)
        Label(self.info_lafr, text=devices_dict['model'],width=30).grid(row=0, column=4)

        Label(self.info_lafr, text='系统版本:').grid(row=1, column=1)
        Label(self.info_lafr, text=devices_dict['version'],width=30).grid(row=1, column=2)

        Label(self.info_lafr, text='SDK版本:').grid(row=1, column=3)
        Label(self.info_lafr, text=devices_dict['sdk_version'],width=30).grid(row=1, column=4)

        Label(self.info_lafr, text='分辨率:').grid(row=2, column=1)
        Label(self.info_lafr, text=devices_dict['display_size'],width=30).grid(row=2, column=2)

        Label(self.info_lafr, text='品牌:').grid(row=2, column=3)
        Label(self.info_lafr, text=devices_dict['manufacturer'],width=30).grid(row=2, column=4)

        self.info_lafr.pack(fill=BOTH, expand=1)

    def __create_appstart_widget(self):
        '''应用启动时间测试控件'''

        self.appstart_lf = LabelFrame(self.frame_top,text='应用启动时间',padx=10, pady=10)
        self.appstart_lf.pack(fill=BOTH,expand=1)
        Label(self.appstart_lf,text='测试次数:').grid(row=0,column=1,pady=10,sticky=E)
        num = [10, 20, 30, 50, 100]
        self.cishu_ac = ttk.Combobox(self.appstart_lf, values=num, state='readonly',width=50)
        self.cishu_ac.current(0)
        self.cishu_ac.grid(row=0,column=2)

        Label(self.appstart_lf, text='包名/Activty:').grid(row=1,column=1)
        self.activity_t = Entry(self.appstart_lf,width=50)
        self.activity_t.grid(row=1,column=2,sticky=W)

        # Label(self.appstart_lf, text='包名').grid(row=2,column=1)
        # self.global_package = Entry(self.appstart_lf,width=50)
        # self.global_package.grid(row=2,column=2,sticky=W)

        start_btn = Button(self.appstart_lf,text='开始测试',command=self.thread_app_start_time)
        start_btn.grid(row=3,column=2,pady=10)


    def __create_appsize_widget(self):
        '''创建 应用ROM 大小控件'''
        self.appsize_lf = LabelFrame(self.frame_top,text='应用ROM',padx=10,pady=10)
        self.appsize_lf.pack(fill=BOTH,expand=1)

        # Label(self.appsize_lf,text='包名').grid(row=0,column=1,pady=10)
        # self.appsize_pck= Entry(self.appsize_lf,width=50)
        # self.appsize_pck.grid(row=0,column=2)

        # self.var = IntVar()
        #
        # self.system_app = tk.Radiobutton(self.appsize_lf, text='内置应用',value=1,variable=self.var)
        # self.system_app.grid(row=1,column=1)
        #
        #
        # self.thirdparty_app = tk.Radiobutton(self.appsize_lf, text='手动安装应用', value=0,variable=self.var)
        # self.thirdparty_app.grid(row=1,column=2)

        start_btn = tk.Button(self.appsize_lf, text='开始测试',command=self.thread_approm)
        start_btn.grid(row=2,column=2)

    def __create_appruning_widget(self):
        '''创建应用运行时RAM'''
        self.apprun_lf = LabelFrame(self.frame_top, text='应用运行时RAM', padx=10, pady=10)
        self.apprun_lf.pack(fill=BOTH,expand=1)
        Label(self.apprun_lf, text='监控间隔时间(分):').grid(row=0, column=1, pady=10, sticky=E)
        num = [2, 4, 6, 8,10,15]
        self.monitoring_time = ttk.Combobox(self.apprun_lf, values=num, state='readonly', width=10)
        self.monitoring_time.current(0)
        self.monitoring_time.grid(row=0, column=2,sticky=W)
        Label(self.apprun_lf, text='监控命令:').grid(row=1, column=1, pady=10, sticky=E)
        self.runcommand = Text(self.apprun_lf, height=3,width=80)
        self.runcommand.insert(END,'adb shell dumpsys meminfo')
        self.runcommand.grid(row=1,column=2,sticky=W)
        Label(self.apprun_lf, text='monkey命令:').grid(row=2,column=1)
        self.monkeycommand = Text(self.apprun_lf, height=4,width=80)
        self.monkeycommand.insert(END,'adb shell monkey -p 包名 -s 10 --pct-touch 30 --throttle 300 -v 10000 --monitor-native-crashes')
        self.monkeycommand.grid(row=2,column=2,pady=10)

        btn_start= Button(self.apprun_lf,text='开始测试',command=self.thread_apprun_ram)
        btn_start.grid(row=3,column=2)

    def __create_appbackrun_wiget(self):
        '''应用后台运行时RAM占用大小'''
        self.appback_lf = LabelFrame(self.frame_top, text='应用后台运行时RAM', padx=10, pady=10)
        self.appback_lf.pack(fill=BOTH, expand=1)
        Label(self.appback_lf, text='监控间隔时间(分):').grid(row=0, column=1, pady=10, sticky=E)
        num = [2,10,15,20,25]
        self.monitoring_time2 = ttk.Combobox(self.appback_lf, values=num, state='readonly', width=10)
        self.monitoring_time2.current(0)
        self.monitoring_time2.grid(row=0, column=2, sticky=W)

        # text='adb shell dumpsys activity activities | findstr[grep] mFocusedActivity'

        Label(self.appback_lf,  text='adb shell dumpsys activity activities | findstr[grep] mFocusedActivity').grid(row=1,column=1,columnspan=2)
        Label(self.appback_lf, text='adb shell dumpsys activity activities | findstr[grep] ResumedActivity(8.0及以上适用)',
              bg='yellow').grid(row=2, column=1, columnspan=2)


        Label(self.appback_lf, text='包名/Activity:').grid(row=3, column=1)
        self.package_av = Text(self.appback_lf, height=1, width=80)
        self.package_av.grid(row=3,column=2)

        Label(self.appback_lf, text='monkey命令:').grid(row=4, column=1)
        self.runcommand2 = Text(self.appback_lf, height=3, width=80)
        self.runcommand2.insert(END,
                                  'adb shell monkey -p 包名 -s 10 --pct-touch 30 --throttle 300 -v 10000 --monitor-native-crashes')
        self.runcommand2.grid(row=4, column=2, pady=10)

        self.btn_start_ram = Button(self.appback_lf, text='开始测试', command=self.thread_appblackrun_ram)
        self.btn_start_ram.grid(row=5, column=2)

        # self.btn_init = Button(self.appback_lf, text='初始化环境', command=self.init_uiautomaotr2)



    def __create_menu_widget(self):
        '''菜单控件'''
        # 创建一个menu
        menubar = Menu(self)
        # 创建一系列的子menu
        lookmenu = Menu(menubar, tearoff=0)
        lookmenu.add_command(label='设备信息', command=self.__show_devices_widget)
        lookmenu.add_command(label='删除', command=self.__delete_pan)

        performance_menu = Menu(menubar, tearoff=0)
        performance_menu.add_command(label='CPU/内存/流量',command=self.__shwo_cpu_widget)
        performance_menu.add_command(label='Monkey测试',command=self.__show_monkey_widget)
        performance_menu.add_command(label='应用启动时间',command=self.__show_appstart_widget)

        qualify_menu = Menu(menubar, tearoff=0)
        qualify_menu.add_command(label='应用ROM',command=self.__show_appsize_widget)
        qualify_menu.add_separator()
        qualify_menu.add_command(label='应用后台运行时RAM',command=self.__show_appbackrun_widget )
        qualify_menu.add_command(label ='应用运行时RAM',command=self.__show_appruning_widget)

        menubar.add_cascade(label='查看', menu=lookmenu)
        menubar.add_cascade(label='性能测试', menu=performance_menu)
        menubar.add_cascade(label='Qualify',menu=qualify_menu)
        self.config(menu=menubar)

    def __show_appbackrun_widget(self):
        '''展示应用后台运行时RAM'''
        self.__delete_pan()
        self.glabel_l['text'] = '程序启动后需要用户手动操作进入用户首页'
        self.glabel_l['fg'] = 'red'
        self.__create_appbackrun_wiget()


    def __show_appruning_widget(self):
        '''展示应用运行时RAM'''
        self.__delete_pan()
        self.__create_appruning_widget()

    def __show_appstart_widget(self):
        '''展示应用启动测试信息'''
        self.__delete_pan()
        self.glabel_l['text']='该功能只适用于Root权限机型'
        self.glabel_l['fg'] = 'red'
        self.__create_appstart_widget()

    def __show_devices_widget(self):
        '''展示设备信息'''
        self.__delete_pan()
        self.__create_devices_widget()

    def __show_monkey_widget(self):
        '''展示monkey控件'''
        self.__delete_pan()
        self.__create_monkey_widget()

    def __shwo_cpu_widget(self):
        '''展示cpu控件'''
        self.__delete_pan()
        self.__create_cpu_widget()

    def __show_appsize_widget(self):
        '''展示获取APK大小控件'''
        self.__delete_pan()
        self.glabel_l['text']='测试前请先检查应用是否已启动过,否则获取信息不全'
        self.glabel_l['fg']='red'
        self.__create_appsize_widget()


    def __delete_pan(self):
        '''删除顶部控件'''
        self.data_text.delete(1.0,END)
        for child in self.frame_top.winfo_children():
            child.pack_forget()

    def thread_appblackrun_ram(self):
        for i in range(1):
            t = threading.Thread(target=self.app_backrun_ram, args=())
            t.start()

    def thread_apprun_ram(self):
        for i in range(1):
            t = threading.Thread(target=self.app_runing_ram, args=())
            t.start()


    def thread_approm(self):
        for i in range(1):
            t = threading.Thread(target=self.app_rom_test, args=())
            t.start()

    def thread_app_start_time(self):
        for i in range(1):
            t = threading.Thread(target=self.app_start_time, args=())
            t.start()

    def thread_cpu_app_test(self):
        for i in range(1):
            t = threading.Thread(target=self.cpu_app_test, args=())
            t.start()


    def app_backrun_ram(self):
        '''应用后台运行时RAM占用大小'''
        packagename = self.entryvar.get().strip()
        runcommand2 = self.runcommand2.get('0.0', END).strip()  # 监控命令
        activity = self.package_av.get('0.0',END).strip()
        sleep_time = int(self.monitoring_time2.get())  # 监控间隔时间

        if len(packagename) <= 5 or len(runcommand2)<=5 or len(activity)<=5 or len(activity)<=5:
            messagebox.showwarning('警告', '请检查参数')
        else:
            ram1,ram2 = get_appbackrunram(packagename,activity,sleep_time)
            text='场景1: %sK / 1024 = %sM \n场景2: %sK / 1024 = %sM\n' %(ram1,round(ram1/1024,2),ram2,round(ram2/1024,2))
            self.data_text.insert(END, text)
            self.data_text.see(END)

            #执行场景3-->并且获取运行时RAM
            os.popen(runcommand2)
            count_list = []  # 次数
            max_list = []
            i=0
            while get_pid():
                current_time = datetime.datetime.now().strftime('%H:%M:%S')
                ram_list = get_apprunram('adb shell dumpsys meminfo', packagename)
                ram_sum = sum(ram_list)
                max_list.append(ram_sum)
                i += 1
                count_list.append(i)
                text = '%s 第%s次 %sK \n' % (current_time, i, ram_sum)
                self.data_text.insert(END, text)
                self.data_text.see(END)
                time.sleep(2 * 60)

            _max = round(max(max_list) / 1024, 2)
            print(max(max_list) / 1024)
            text1 = '最大值:%sK / 1024 = %sM\n' % (max(max_list), _max)
            self.data_text.insert(END, text1)
            self.data_text.see(END)
            #执行场景3-->获取后台运行RAM
            ram3 = get_appbackrunram2(packagename,sleep_time)
            text3 = '场景3: %sK / 1024 = %sM'%(ram3,round(ram3/1024,2))
            self.data_text.insert(END,text3)
            self.data_text.see(END)
            messagebox.showinfo('提醒', '测试完成')

    def app_runing_ram(self):
        '''获取应用运行时RAM占用大小'''
        packagename = self.global_package.get().strip()
        runcommand = self.runcommand.get('0.0',END).strip() #监控命令
        monkeycommand = self.monkeycommand.get('0.0',END).strip()#monkey命令
        sleep_time = int(self.monitoring_time.get()) #监控间隔时间

        if len(packagename) <= 5 or len(runcommand)<=5 or len(monkeycommand)<=5:
            messagebox.showwarning('警告', '请检查参数')
        else:
            count_list = []  #次数
            max_list = []

            #运行monkey命令
            os.popen(monkeycommand)
            time.sleep(2)
            i=0
            while get_pid():
                current_time = datetime.datetime.now().strftime('%H:%M:%S')
                ram_list = get_apprunram(runcommand,packagename)
                ram_sum = sum(ram_list)
                max_list.append(ram_sum)
                i+=1
                count_list.append(i)
                text = '%s 第%s次 %sK \n'%(current_time,i,ram_sum)
                self.data_text.insert(END,text)
                self.data_text.see(END)
                time.sleep(sleep_time * 60)

            _max = round(max(max_list) / 1024, 2)
            print(max(max_list) / 1024)
            text1 = '最大值:%sK / 1024 = %sM' % (max(max_list), _max)
            self.data_text.insert(END, text1)
            self.data_text.update()
            messagebox.showinfo('提醒', '测试完成')



    def app_rom_test(self):
        '''获取应用ROM占用大小'''
        devices_status = getDevicesStatus()
        if devices_status == 'device':
            packagename = self.global_package.get()
            if len(packagename) <= 5:
                LOG.info('包名必须真实有效')
                messagebox.showwarning('警告', '请检查您的包名')
            else:
                rslist, apksize = get_appsize(packagename)
                print(rslist)
                for i in rslist:
                    self.data_text.insert(END, i)
                    self.data_text.insert(END, '\n')

    def cpu_app_test(self):
        status_devices = getDevicesStatus()
        self.__running = True
        if status_devices == 'device':
            # cpupackagename = self.cpu_packagename_t.get()

            cpupackagename = self.global_package.get()
            print(cpupackagename)
            sleep_time = int(self.intervatime_t.get())  # 间隔时间
            chixun_time = int(self.chixuntime_t.get())  # 持续执行时间
            if len(cpupackagename) <= 5:
                LOG.info('包名必须真实有效')
                messagebox.showwarning('警告', '请检查您的包名')
            else:
                cishu_list = []
                cpu_list = []
                rescv_list = []
                send_list = []
                total_list = []
                pass_list = []
                i = 0
                current_time = datetime.datetime.now()
                time_end = current_time + datetime.timedelta(minutes=chixun_time)  # 最后结束时间

                while self.__running and contrast(current_time,time_end):
                    hour = datetime.datetime.now().strftime('%H:%M:%S')
                    memory = getMemory(cpupackagename)
                    rescv, send, flow_sum = getFlow(cpupackagename)
                    cpu = getCpu(cpupackagename)

                    self.cpu_btn_start['state'] = 'disabled'
                    self.cpu_btn_stop['state'] = 'normal'

                    cpu_list.append(float(cpu.split('%')[0]))
                    pass_list.append(int(memory[:-1]))
                    total_list.append(int(flow_sum))
                    rescv_list.append(int(rescv))
                    send_list.append(int(send))

                    text = '%s   cpu:%s   Pass:%s  总流量:%sk,  上传流量:%sk,  下载流量:%sk' % (
                    hour, cpu, memory, flow_sum, rescv, send)
                    self.data_text.insert(END, text)
                    self.data_text.insert(END, "\n")
                    self.data_text.update()
                    cishu_list.append(hour)

                    time.sleep(sleep_time)
                    current_time = datetime.datetime.now()

                saveCpuResult(cishu=cishu_list, start_cpu=cpu_list, recv_list=rescv_list, send_list=send_list,
                              total_list=total_list,
                              Pass_list=pass_list)

                self.cpu_btn_start['state'] = 'normal'
                LOG.info('测试完成')
                messagebox.showinfo('提醒', '测试完毕，测试报告已经生成！')

        else:
            LOG.info('测试的设备必须正常连接，请注意')
            messagebox.showwarning('警告', '设备连接异常 请重新连接设备!')


    def app_start_time(self):
        start_tim = []
        cishu = []
        status_devices = getDevicesStatus()
        if status_devices == 'device':
            try:
                packname = self.global_package.get().strip()
                print(packname)
                acti = self.activity_t.get().strip()
                cish = self.cishu_ac.get()

            except:
                LOG.info('获取不到测试数据，请检查！')
                messagebox.showinfo('提醒', '获取不到测试数据，请检查！')
            if len(acti) <= 1 or len(packname) <= 1:
                messagebox.showinfo('提醒', '包命或者包名activity不能为空')
                LOG.info('包命或者包名activity不能为空')
            else:
                if len(cish) <= 1:
                    messagebox.showinfo('提醒', '次数不能为空')
                    LOG.info('次数不能为空')
                else:
                    i = 0
                    # e1['state'] = 'normal'
                    # e1.delete(1.0, tkinter.END)
                    sum = 0
                    for i in range(int(cish)):
                        start_time = starttime_app(packagename=packname, packagenameactivicy=acti)
                        start_tim.append(int(start_time[1]))

                        cishu.append(i)
                        if start_time is None:
                            messagebox.showwarning('警告', '请检查您输入的包或者包的启动activity')
                            break
                        text = '第%s次启动时间：%s' % (i + 1, start_time[1])
                        LOG.info('第%s次启动时间：%s' % (i + 1, start_time[1]))
                        sum += int(start_time[1])
                        # e1['state'] = 'normal'

                        self.data_text.insert(END,text)
                        self.data_text.insert(END,'\n')

                        self.data_text.update()
                        # btn_start['state'] = 'disabled'
                    self.data_text.insert(END, ('平均用时:%s ms' % (sum / int(cish))))
                    LOG.info(('平均用时:%s' % (sum / int(cish))))
                    saveStartAppResult(cishu=cishu, start=start_tim)
                    messagebox.showinfo('提示', '测试报告已经生成，请到当前目录查看')
                    LOG.info('测试报告已经生成，请到当前目录查看')
                    # e1['state'] = 'disabled'
                    # btn_start['state'] = 'normal'
                    messagebox.showinfo('通知', '测试已经完成')
                    LOG.info('测试已经完成')
        else:
            messagebox.showerror('警告', '设备连接异常')
            LOG.info('设备连接异常')


    def thread_stop(self):
        self.__running =False
        LOG.info('self.__running %s'%self.__running)

    def monkey_app(self):
        devices_status = getDevicesStatus()
        if devices_status == 'device':
            try:
                packname = self.package_t1.get('0.0', END).split()[0]
                zhongzi = self.zhongzi_t.get('0.0', END).split()[0]
                time = self.time_t.get().split()[0]
                touch = self.touch_t.get('0.0', END).split()[0]
                huadong = self.huadong_t.get('0.0', END).split()[0]
                guiji = self.trackball_t.get('0.0', END).split()[0]
                xitong = self.xitong_t.get('0.0', END).split()[0]
                acti = self.acti_t.get('0.0', END).split()[0]
                event = self.event_t.get('0.0', END).split()[0]
                log = self.log_t.get('0.0', END).split()[0]
                danghang = self.danghang_t.get('0.0', END).split()[0]
                if len(packname) <= 5:
                    LOG.info('请正确填写包名')
                    messagebox.showwarning('提醒', '请正确填写包名')
                if int(touch) + int(huadong) + int(guiji) + int(danghang) + int(xitong) + int(acti) > 100:
                    messagebox.showerror('提醒', '您输入的所有的事件的比例和不能超过100%')
                    LOG.info('您输入的所有的事件的比例和不能超过100')
                run_monkey(packagename=packname, s_num=zhongzi, throttle=time, pct_touch=touch, pct_motion=huadong,
                           pct_trackball=guiji, pct_nav=danghang, pct_syskeys=xitong, pct_appswitch=acti, num=event,
                           logfilepath=log)
            except:
                messagebox.showwarning('警告', '必须填写monkey相关数据')
                LOG.info('monkey 测试出错，原因:%s' % Exception)
        else:
            LOG.info('设备连接异常 请重新连接设备!')
            messagebox.showwarning('警告', '设备连接异常 请重新连接设备!')


if __name__ == '__main__':

    devices = getdevices_list()
    if len(devices) > 0 :
        app = Application(devices=devices)
        app.title("测试工具")
        tmp = open("tmp.ico", "wb+")
        tmp.write(base64.b64decode(img))
        tmp.close()

        app.iconbitmap('tmp.ico')

        app.mainloop()
        os.remove("tmp.ico")
    else:
        messagebox.showinfo('警告', '请先连接手机')


