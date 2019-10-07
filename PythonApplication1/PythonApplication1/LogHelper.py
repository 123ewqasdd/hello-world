#!/usr/bin/python3 
# -*- coding:utf-8 -*-
import logging

class LogHelper:

    def __init__(self, logName="logs.txt"):
        LOG_FORMAT =  "%(asctime)s - %(levelname)s - %(message)s"  
        DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"                       
        fp = logging.FileHandler(logName, encoding='utf-8')
        fs = logging.StreamHandler()
        logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[fp, fs])  


    @staticmethod
    def debug(msg):
        logging.debug(msg)

    @staticmethod
    def info(msg):
        logging.info(msg)

    @staticmethod
    def warning(msg):
        logging.warning(msg)
        
    @staticmethod
    def error(msg):
        logging.error(msg)

    @staticmethod
    def critical(msg):
        logging.critical(msg)



#import logging
#LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"    # 日志格式化输出
#DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"                        # 日期格式
#fp = logging.FileHandler('a.txt', encoding='utf-8')
#fs = logging.StreamHandler()
#logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[fp, fs])    # 调用


#logging.debug("This is a debug log.哈哈")
#logging.info("This is a info log.")
#logging.warning("This is a warning log.")
#logging.error("This is a error log.")
#logging.critical("This is a critical log.")