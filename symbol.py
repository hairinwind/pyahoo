from os import environ
from util.logger import logger
import datetime
import numpy as np
import requests

symbolDir = 'config/'

def getSymbolFileName():
    if environ.get('PYAHOO_SYMBOL_FILE'):
        return environ.get('PYAHOO_SYMBOL_FILE')
    else:
        return 'symbol_test.txt'

def readSymbolsFromFile():
    symbol_file_name = getSymbolFileName()
    # read symbol from git
    if not symbol_file_name:
        symbol_file_name = "symbol.txt"
    baseUrl = 'https://raw.githubusercontent.com/hairinwind/pyahoo/master/config/'
    url = baseUrl + symbol_file_name
    logger.info("symbol_file: " + url)
    symbol_text = requests.get(url).content.decode("utf-8")
    symbols = symbol_text.splitlines()
    symbols = np.unique(symbols)
    now = datetime.datetime.now()
    print("minute: " + str(now.minute))
    print(symbols)
    return symbols

if __name__=="__main__":
    symbols = readSymbolsFromFile()
    logger.info(symbols)
    logger.info(symbols[0])