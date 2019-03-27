from os import environ
import numpy as np

def getSymbolFileName():
    print('read env variable:', 'PYAHOO_SYMBOL_FILE')
    if environ.get('PYAHOO_SYMBOL_FILE'):
        return environ.get('PYAHOO_SYMBOL_FILE')
    else:
        return 'symbol.txt'

def readSymbolsFromFile():
    symbolFileName = getSymbolFileName()
    print('- read symbols from %s' % symbolFileName)
    symbols = np.loadtxt(symbolFileName, dtype='str')
    return np.unique(symbols)

if __name__=="__main__":
    symbols = readSymbolsFromFile()
    print(symbols)
    print(symbols[0])