import datetime
import threading
from functools import partial

# use EST or EDT
marketOpenHour = 4
marketOpenMinute = 00
marketCloseHour = 20 
marketCloseMinute = 30


###
# this is the method to determine when it shall collect the quote 
###
def startJob(jobFunc):
    nextCollectTime = getNextCollectTime()
    print('-- next collect time is ', nextCollectTime)
    timeDelta = (nextCollectTime - current()).seconds

    # start thread 
    threading.Timer(timeDelta, runJob, [jobFunc]).start()
    print('-- new thread is started to run the job')

def runJob(jobFunc):
    threading.Timer(300, runJob, [jobFunc]).start()
    now = current()
    todayOpen = now.replace(hour=marketOpenHour, minute=marketOpenMinute, second=0, microsecond=0)
    todayEnd = now.replace(hour=marketCloseHour, minute=marketCloseMinute, second=0, microsecond=0)
    if now >= todayOpen and now <= todayEnd:
        jobFunc()

def getNextCollectTime(): 
    now = current()
    next5min = now + datetime.timedelta(minutes=5)
    minute = next5min.minute // 5 * 5
    return next5min.replace(minute=minute, second=0, microsecond=0)

def current():
    return datetime.datetime.now()


if __name__=="__main__":
	pass