from os import listdir
from os.path import isfile, join

def run(): 
    onlyfiles = [f for f in listdir('quotes') if isfile(join('quotes', f))]
    for f in onlyfiles: 
        num_lines = sum(1 for line in open('quotes/'+f))
        print(f, num_lines)

if __name__=="__main__":
	run()