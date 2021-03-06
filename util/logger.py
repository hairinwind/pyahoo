import logging
import time
from logging.handlers import TimedRotatingFileHandler
from util import envUtil
 
logger = logging.getLogger()

def initLogger(path='log/pyahoo.log'):
    if envUtil.isDev():
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        
    # format the log entries
    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s')
 
    handler = TimedRotatingFileHandler(path,
                                       when='midnight',
                                       backupCount=10)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)