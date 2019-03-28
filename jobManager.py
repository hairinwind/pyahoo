import threading
from functools import partial
from util import dateUtil, envUtil
from util.logger import logger

"""
this is the job to collect the quote 
"""
def startJob(jobFunc):
    nextCollectTime = dateUtil.getNextCollectTime()
    logger.debug('-- next collect time is %s' % nextCollectTime)
    timeDelta = (nextCollectTime - dateUtil.current()).seconds

    # start thread 
    threading.Timer(timeDelta, runJob, [jobFunc]).start()

def runJob(jobFunc):
    intervals = 300
    if envUtil.isDev():
        intervals = 30
    threading.Timer(intervals, runJob, [jobFunc]).start()
    logger.debug('current %s' % dateUtil.current())
    logger.debug('beforeEndTime %s' % dateUtil.beforeEndTime())
    logger.debug('afterStartTime %s' % dateUtil.afterStartTime())
    logger.debug('wait... %s' % intervals)
    if dateUtil.beforeEndTime() and dateUtil.afterStartTime():
        jobFunc()

def test():
    logger.info('test')

if __name__=="__main__":
    startJob(test)