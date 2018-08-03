#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/12 13:21
# @Author  : qingping.niu
# @File    : log.py
# @desc    : 日志记录打印

import os
from functools import wraps   #装饰器
import logbook
from logbook import Logger,StreamHandler,FileHandler,TimedRotatingFileHandler
from logbook.more import ColorizedStderrHandler  #日志打印到屏幕


def log_type(record,handler):
    log = "[{date}] [{level}] [{filename}] [{func_name}] [{lineno}] {msg}".format(
        date = record.time,                              # 日志时间
        level = record.level_name,                       # 日志等级
        filename = os.path.split(record.filename)[-1],   # 文件名
        func_name = record.func_name,                    # 函数名
        lineno = record.lineno,                          # 行号
        msg = record.message                             # 日志内容
    )
    return log

#日志存放路径
LOG_DIR = os.path.join('.','log')
file_stream = False
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
    file_stream = True

# # 日志打印到屏幕
log_std = ColorizedStderrHandler(bubble=True)
log_std.formatter = log_type

# 日志打印到文件
log_file = TimedRotatingFileHandler(
    os.path.join(LOG_DIR, '%s.log' % 'log'),date_format='%Y-%m-%d', bubble=True, encoding='utf-8')
log_file.formatter = log_type


run_log = Logger('script_log')
def init_logger():
    """ get logger Factory function """
    logbook.set_datetime_format("local")#格式化时间
    run_log.handlers = []
    run_log.handlers.append(log_file)
    run_log.handlers.append(log_std)
    return run_log


# run_log = Logger('script_log')
# def init_logger():
#     """ get logger Factory function """
#     logbook.set_datetime_format("local")#格式化时间
#     run_log.handlers = []
#     run_log.handlers.append(log_file)
#     run_log.handlers.append(log_std)


# 实例化，默认调用
LOG = init_logger()


# def get_logger(name='打印日志',file_log=file_stream,level = ''):
#     """ get logger Factory function """
#     logbook.set_datetime_format("local")  #格式化时间
#
#     ColorizedStderrHandler(bubble=True, level=level).push_thread() #bubble=False屏幕不打印日志
#     logbook.TimedRotatingFileHandler(
#         os.path.join(LOG_DIR, '%s.log' % name),
#         date_format='%Y-%m-%d-%H', bubble=True, encoding='utf-8').push_thread()  #日志打印到文件
#     return logbook.Logger(name)
# #
# LOG = get_logger(file_log=file_stream, level='INFO')


def logger(param):
    """ fcuntion from logger meta """
    def wrap(function):
        """ logger wrapper """
        @wraps(function)
        def _wrap(*args, **kwargs):
            """ wrap tool """
            LOG.info("当前模块 {}".format(param))
            LOG.info("全部args参数参数信息 , {}".format(str(args)))
            LOG.info("全部kwargs参数信息 , {}".format(str(kwargs)))
            return function(*args, **kwargs)
        return _wrap
    return wrap

