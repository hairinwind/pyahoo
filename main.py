from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from functools import partial
from jobManager import startJob
from pemail import gmailapi 
from symbol import getSymbolFileName, readSymbolsFromFile
from util.fileManager import runFuncSynchronized
from util.logger import initLogger, logger
from util import envUtil
from yahoo_finance import parse
import json
import os
import pandas as pd
import random
import threading

# threads = []
def collectQuotes(symbols): 
    for symbol in symbols: 
        # start new thread to coolect Quote
        threading.Thread(target=getAndSaveQuote, args=[symbol]).start()

def getAndSaveQuote(symbol):
    quote = parse(symbol)
    # save
    date = datetime.now().strftime('%Y%m%d')
    fileName = 'quotes/'+symbol + '_' + date+ '.json'
    runFuncSynchronized(saveQuote, quote, fileName)

def saveQuote(data, fileName):
    with open(fileName, 'a') as f:
        f.write(json.dumps(data) + '\n')

def run():
    printEnv()
    symbols = readSymbolsFromFile()
    jobFunc = partial(collectQuotes, symbols)
    startJob(jobFunc)
    emailFiles()

def emailJob():
    randomWait = random.randint(0, 600)
    sleep(randomWait)
    logger.debug('emailJob is running...')
    date = datetime.now().strftime('%Y%m%d')
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

if __name__=="__main__":
    initLogger()
    run()