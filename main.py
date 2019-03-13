from datetime import datetime
from functools import partial
from jobManager import startJob
from pemail import gmail 
from symbol import readSymbolsFromFile
from util.fileManager import runFuncSynchronized
from yahoo_finance import parse
import json
import pandas as pd
import os
import threading

# threads = []
def collectQuotes(symbols): 
    for symbol in symbols: 
        # start new thread to coolect Quote
        threading.Thread(target=getAndSaveQuote, args=[symbol]).start()

def getAndSaveQuote(symbol):
#     print(symbol+'  ', datetime.utcnow())
    quote = parse(symbol)
    # save
    date = datetime.now().strftime('%Y%m%d')
    fileName = 'quotes/'+symbol + '_' + date+ '.json'
    runFuncSynchronized(saveQuote, quote, fileName)

def saveQuote(data, fileName):
    with open(fileName, 'a') as f:
        f.write(json.dumps(data) + '\n')

def run():
    symbols = readSymbolsFromFile()
    jobFunc = partial(collectQuotes, symbols)
    startJob(jobFunc)

def emailJob():
    date = datetime.now().strftime('%Y%m%d')
    files = os.listdir('quotes')
    files = [file for file in files if date in file]
    gmail.send_email_text('rbcFund','', filename=files)

def emailFiles():
    print('emailFiles is running...')
    scheduler = BlockingScheduler()
	scheduler.add_job(emailJob, 'cron', day_of_week='1-5', hour=23, minute=0)
	scheduler.start()

if __name__=="__main__":
	run()
    emailFiles() 
    # for t in threads:
    #     t.join()
