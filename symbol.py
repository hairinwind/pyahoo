import numpy as np

def readSymbolsFromFile():
    print('- read symbols from symbol.txt')
    symbols = np.loadtxt('symbol.txt', dtype='str')
    return np.unique(symbols)

if __name__=="__main__":
    symbols = readSymbolsFromFile()
    print(symbols)
    print(symbols[0])