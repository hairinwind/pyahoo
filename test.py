import threading
import datetime
from functools import partial
from jobManager import startJob

def testFunc(arg1):
    print(datetime.datetime.now(), threading.currentThread().getName(), arg1)

def run():
    for i in range(10):
        jobFunc = partial(testFunc, i)
        startJob(jobFunc)

if __name__=="__main__":
	run()