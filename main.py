from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from functools import partial
from jobManager import startJob
from os import environ
from pemail import gmailapi 
from symbol import getSymbolFileName, readSymbolsFromFile
from time import sleep
from util.fileManager import runFuncSynchronized
from util.logger import initLogger, logger
from util import dateUtil, envUtil
# from yahoo_finance import parse
from finnhub import parse
import json
import os
import pandas as pd
import random
import threading
import time

API_KEY = environ.get('FINNHUB_API_KEY')# 'c7ce9oqad3idhma69mog'

# threads = []
def collectQuotes():
    symbols = readSymbolsFromFile() 
    for index, symbol in enumerate(symbols): 
        # start new thread to coolect Quote
        if int(index/60) == index / 60:
            time.sleep(61)
        threading.Thread(target=getAndSaveQuote, args=[symbol]).start()

def getAndSaveQuote(symbol):
    toTime = datetime.now() # (2022,1,13,13,0,0,0)
    quote = parse(symbol, API_KEY, toTime)
    if quote is not None:
        # save
        date = dateUtil.current().strftime('%Y%m%d')
        fileName = 'quotes/'+symbol + '_' + date+ '.json'
        runFuncSynchronized(saveQuote, quote, fileName)

def saveQuote(data, fileName):
    with open(fileName, 'a') as f:
        f.write(json.dumps(data) + '\n')

def run():
    printEnv()
    # symbols = readSymbolsFromFile()
    # jobFunc = partial(collectQuotes, symbols)
    startJob(collectQuotes)
    # emailFiles()

def emailJob():
    randomWait = random.randint(0, 600)
    sleep(randomWait)
    logger.debug('emailJob is running...')
    date = dateUtil.current().strftime('%Y%m%d')
    files = os.listdir('quotes')
    files = ['quotes/'+file for file in files if date in file]
    logger.debug('going to send email', files)
    gmailapi.send('stock 5 minutes','', files=files)

def emailFiles():
    logger.debug('email task is scheduled...')
    scheduler = BlockingScheduler()
    scheduler.add_job(emailJob, 'cron', day_of_week='1-5', hour=21, minute=30)
    scheduler.start()

def printEnv():
    logger.info('PYAHOO_ENV: %s' % envUtil.getPyahooEnv())
    logger.info('symbol file name: %s' % getSymbolFileName())
    logger.info('finnhub API key: %s' % API_KEY)

if __name__=="__main__":
    if API_KEY is None:
        raise Exception('finnhub api key is not configured as env variable...')
    initLogger()
    run()
    