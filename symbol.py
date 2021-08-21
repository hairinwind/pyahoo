from os import environ
from util.logger import logger
import numpy as np
import requests

symbolDir = 'config/'

def getSymbolFileName():
    if environ.get('PYAHOO_SYMBOL_FILE'):
        return environ.get('PYAHOO_SYMBOL_FILE')
    else:
        return 'symbol.txt'

def readSymbolsFromFile():
    symbol_file_name = getSymbolFileName()
    if symbol_file_name.startswith('http'):
        # read file from remote
        symbol_text = requests.get(symbol_file_name).content.decode("utf-8")
        symbols = symbol_text.splitlines()
        symbols = np.unique(symbols)
        return symbols
    else:
        symbolFileName = symbolDir + symbol_file_name
        symbols = np.loadtxt(symbolFileName, dtype='str')
        return np.unique(symbols)

if __name__=="__main__":
    symbols = readSymbolsFromFile()
    logger.info(symbols)
    logger.info(symbols[0])