from datetime import datetime, timedelta
from util import envUtil

# use EST or EDT
preMarketStart = datetime.now().replace(hour=4, minute=0, second=0, microsecond=0)
marketOpen = datetime.now().replace(hour=9, minute=30, second=0, microsecond=0)
marketClose = datetime.now().replace(hour=16, minute=0, second=0, microsecond=0)
postMarketEnd = datetime.now().replace(hour=20, minute=30, second=0, microsecond=0)

def current():
    return datetime.now()

def getNextCollectTime():
    if envUtil.isDev():
        return current() + timedelta(seconds=5)
    now = current()
    next5min = now + timedelta(minutes=5)
    minute = next5min.minute // 5 * 5
    return next5min.replace(minute=minute, second=0, microsecond=0)

def beforeEndTime():
    return current() <= postMarketEnd
    
def afterStartTime():
    return current() >= preMarketStart

def isPreMarket():
    now = current()
    return preMarketStart <= now < marketOpen

def isPostMarket():
    now = current()
    return marketClose < now <= postMarketEnd
