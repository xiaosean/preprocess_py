#coding:utf-8
import os
import logging
LOG_DIR = "LOG"
if not os.path.exists(os.path.join(LOG_DIR)):
    os.makedirs(LOG_DIR)
# BASE_DIR = os.path.dirname(os.path.join(LOG_DIR))
BASE_DIR = os.path.join(LOG_DIR)

DEBUG = True #标记是否在开发环境
 
#给过滤器使用的判断
class RequireDebugTrue(logging.Filter):
    #实现filter方法
    def filter(self, record):
        return DEBUG
 
 
LOGGING = {
    #基本设置
    'version':1, #日志级别
    'disable_existing_loggers':False, #是否禁用现有的记录器
    
    #日志格式集合
    'formatters':{ 
        #标准输出格式
        'standard':{
            #[具体时间][线程名:线程ID][日志名字:日志级别名称(日志级别ID)] [输出的模块:输出的函数]:日志内容
            'format':'[%(asctime)s][%(threadName)s:%(thread)d][%(name)s:%(levelname)s(%(lineno)d)]\n[%(module)s:%(funcName)s]:%(message)s'
        }
    },
    
    #过滤器
    'filters':{
        'require_debug_true': {
            '()': RequireDebugTrue,
        }
    },
    
    #处理器集合
    'handlers':{ 
        #输出到控制台
        'console':{
            'level':'DEBUG',    #输出信息的最低级别
            'class':'logging.StreamHandler',
            'formatter':'standard', #使用standard格式
            'filters': ['require_debug_true',], #仅当 DEBUG = True 该处理器才生效
        },
        #输出到文件
        'log':{
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'formatter':'standard',
            # 'filename':os.path.join(BASE_DIR, 'debug.log'), #输出位置
            'filemode':'w+',
            'filename':'LOG\debug.log', #输出位置
            'maxBytes':1024*1024*5, #文件大小 5M
            'backupCount': 5, #备份份数
            'encoding': 'utf8', #文件编码
        },
    },
    
    #日志管理器集合
    'loggers':{
        #管理器
        'default':{
            'handlers':['console', 'log'],
            'level':'DEBUG',
            'propagate':True, #是否传递给父记录器
        },
    }
}