import threading
from functools import partial
from util import dateUtil

###
# this is the method to determine when it shall collect the quote 
###
def startJob(jobFunc):
    nextCollectTime = dateUtil.getNextCollectTime()
    print('-- next collect time is ', nextCollectTime)
    timeDelta = (nextCollectTime - dateUtil.current()).seconds

    # start thread 
    threading.Timer(timeDelta, runJob, [jobFunc]).start()
    print('-- new thread is started to run the job')

def runJob(jobFunc):
    threading.Timer(300, runJob, [jobFunc]).start()
    if dateUtil.beforeEndTime() and dateUtil.afterStartTime():
        jobFunc()

if __name__=="__main__":
	pass