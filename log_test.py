#coding:utf-8
import logging
import logging.config
import log_config

#加载前面的标准配置
LOGGING = log_config.LOGGING
logging.config.dictConfig(LOGGING)
 
#获取loggers其中的一个日志管理器
logger = logging.getLogger("default")
 
#尝试写入不同消息级别的日志信息
logger.debug("debug message")
logger.info("info message")
logger.warning("warn message")
logger.error("error message")
logger.critical("critical message")