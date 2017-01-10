#-*- coding:utf-8 -*-
'''
import logging

logger = logging.getLogger("Trader")
logger.setLevel(logging.DEBUG)

#  这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志
if not logger.handlers:
    # 建立一个filehandler来把日志记录在文件里，级别为debug以上
    fh = logging.FileHandler("./log/sample.log",mode='w')
    fh.setLevel(logging.INFO)
    # 建立一个streamhandler来把日志打在CMD窗口上，级别为error以上
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # 设置日志格式
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    #将相应的handler添加在logger对象中
    logger.addHandler(ch)
    logger.addHandler(fh)
# 开始打日志

def log(message):
    logger.error(message)
    
logger.debug("debug message")
logger.info("info message")
logger.warn("warn message")
logger.error("error message")
logger.critical("critical message")

logger.handlers.pop()
logger.handlers.pop()
logging.shutdown()

    '''
def TestRotating():
    import logging
    import logging.handlers
    
    LOG_FILENAME = './log/logging_file.log'
    # Set up a specific logger with our desired output level
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.DEBUG)
    # Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,mode='a',maxBytes=20, backupCount=5)
    my_logger.addHandler(handler)
    # Log some messages
    for i in range(20):
        my_logger.debug('i = %d' % i)
    my_logger.handlers.pop()
    logging.shutdown() 

TestRotating()       
#log("aaa")