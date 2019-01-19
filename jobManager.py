import datetime
import threading
from functools import partial

marketOpenHour = 14
marketOpenMinute = 25
marketCloseHour = 21 
marketCloseMinute = 30


###
# this is the method to determine when it shall collect the quote 
###
def startJob(jobFunc):
    nextCollectTime = getNextCollectTime()
    print('-- next collect time is ', nextCollectTime)
    timeDelta = (nextCollectTime - utcNow()).seconds
    # xxxxxxxxxxxxx
    timeDelta = 2

    # start thread 
    threading.Timer(timeDelta, runJob, [jobFunc]).start()
    print('-- new thread is started to run the job')

count = 0
def runJob(jobFunc):
    # xxxxxxxxxxxxxxxxx
    threading.Timer(30, runJob, [jobFunc]).start()
    now = utcNow()
    todayOpen = now.replace(hour=marketOpenHour, minute=marketOpenMinute, second=0, microsecond=0)
    todayEnd = now.replace(hour=marketCloseHour, minute=marketCloseMinute, second=0, microsecond=0)
    # xxxxxxxxxxxxxxxxxxx
    # if now >= todayOpen and now <= todayEnd:
    global count 
    count = count + 1
    if count <= 300:
        print('count', count)
        jobFunc()

def getNextCollectTime(): 
    now = utcNow()
    next5min = now + datetime.timedelta(minutes=5)
    minute = next5min.minute // 5 * 5
    return next5min.replace(minute=minute, second=0, microsecond=0)

def utcNow():
    return datetime.datetime.utcnow()


if __name__=="__main__":
	pass