from symbol import readSymbolsFromFile
from jobManager import startJob
from datetime import datetime
from functools import partial
from yahoo_finance import parse
import threading
import pandas as pd
import os

def collectQuotes(symbols): 
    for symbol in symbols: 
        # start new thread to coolect Quote
        threading.Thread(target=getAndSaveQuote, args=[symbol]).start()

def getAndSaveQuote(symbol):
    quote = parse(symbol)
    df = pd.DataFrame(quote, columns=quote.keys())
    # save
    date = datetime.now().strftime('%Y%m%d')
    fileName = 'quotes/'+symbol + '_' + date+ '.csv'
    needHeader = not (os.path.isfile(fileName) and os.path.getsize(fileName) > 0)
    with open(fileName, 'a') as f:
        df.to_csv(f, header=needHeader)

def run():
    symbols = readSymbolsFromFile()
    jobFunc = partial(collectQuotes, symbols)
    startJob(jobFunc)

if __name__=="__main__":
	run()
