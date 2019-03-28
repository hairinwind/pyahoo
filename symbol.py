from os import environ
from util.logger import logger
import numpy as np

symbolDir = 'config/'

def getSymbolFileName():
    if environ.get('PYAHOO_SYMBOL_FILE'):
        return environ.get('PYAHOO_SYMBOL_FILE')
    else:
        return 'symbol.txt'

def readSymbolsFromFile():
    symbolFileName = symbolDir + getSymbolFileName()
    symbols = np.loadtxt(symbolFileName, dtype='str')
    return np.unique(symbols)

if __name__=="__main__":
    symbols = readSymbolsFromFile()
    logger.info(symbols)
    logger.info(symbols[0])