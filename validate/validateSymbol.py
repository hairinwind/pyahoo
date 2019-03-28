from symbol import readSymbolsFromFile
from jobManager import startJob
from datetime import datetime
from functools import partial
from yahoo_finance import parse
import threading
import pandas as pd
import os
import urllib3


def validateQuote(symbol):
#     print(symbol+'  ', datetime.utcnow())
    quote = parse(symbol)
    if not quote['price']:
        print(symbol) 

def run():
    symbols = readSymbolsFromFile()
    for symbol in symbols:
        validateQuote(symbol)

if __name__=="__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    run()
