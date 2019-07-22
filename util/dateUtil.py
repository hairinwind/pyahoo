from datetime import datetime, timedelta
from pytz import timezone
from util import envUtil

# use EST or EDT
def getPreMarketStart(): 
    return current().replace(hour=4, minute=0, second=0, microsecond=0)

def getMarketOpen(): 
    return current().replace(hour=9, minute=30, second=0, microsecond=0)

def getMarketClose():
    return current().replace(hour=16, minute=0, second=0, microsecond=0)

def getPostMarketEnd():
    return current().replace(hour=20, minute=30, second=0, microsecond=0)

def current():
    return datetime.now().astimezone(timezone('America/Toronto'))

def getNextCollectTime():
    if envUtil.isDev():
        return current() + timedelta(seconds=5)
    now = current()
    next5min = now + timedelta(minutes=5)
    minute = next5min.minute // 5 * 5
    return next5min.replace(minute=minute, second=0, microsecond=0)

def beforeEndTime():
    if envUtil.isDev():
        return True
    return isWeekday(current()) and current() <= getPostMarketEnd()
    
def afterStartTime():
    if envUtil.isDev():
        return True
    return isWeekday(current()) and current() >= getPreMarketStart()

def isPreMarket():
    now = current()
    return getPreMarketStart() <= now < getMarketOpen()

def isPostMarket():
    now = current()
    return getMarketClose() < now <= getPostMarketEnd()

def isWeekday(date):
    return date.weekday() < 5