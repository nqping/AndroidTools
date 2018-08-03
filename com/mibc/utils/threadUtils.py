#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/14 17:25
# @Author  : qingping.niu
# @File    : threadUtils.py
# @desc    :

import threading,time
from com.mibc.adb.adbCommand import getCpu,getMemory,getFlow

class ThreadUtils(threading.Thread):

    def __init__(self,*avgs,**kwargs):
        threading.Thread.__init__(self)
        self.avgs = avgs
        self.__flag = threading.Event()  # 用于暂停线程的标识
        self.__flag.set()  # 设置为True
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()  # 将running设置为True

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()
            print(self.avgs[0])
            self.cpu_result = getCpu(self.avgs[0])
            self.mem_result = getMemory(self.avgs[0])
            self.flow_result = getFlow(self.avgs[0])
            # print(self.cpu_result,self.mem_result,self.flow_result)
            self.get_result()

            time.sleep(3)


    def get_result(self):
        print("*********")
        try:
            return self.cpu_result, self.mem_result, self.flow_result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None

    def pause(self):
        self.__flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.clear()  # 设置为False, 让线程阻塞
        self.__flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()  # 设置为False



# if __name__=='__main__':
#     t = ThreadUtils('com.tcl.joylockscreen')
#     t.start()
#     t.join()
#     result = t.get_result()
#
#     print('----------',result)






