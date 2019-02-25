from symbol import readSymbolsFromFile
from jobManager import startJob
from datetime import datetime
from functools import partial
from yahoo_finance import parse
import threading
import pandas as pd
import os
import json
from util.fileManager import runFuncSynchronized

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

if __name__=="__main__":
    run()
    # for t in threads:
    #     t.join()
