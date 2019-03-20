from datetime import datetime

# use EST or EDT
preMarketStart = current().replace(hour=4, minute=0, second=0, microsecond=0)
marketOpen = current().replace(hour=9, minute=30, second=0, microsecond=0)
marketClose = current().replace(hour=16, minute=0, second=0, microsecond=0)
postMarketEnd = current().replace(hour=20, minute=30, second=0, microsecond=0)

def current():
    return datetime.now()

def getNextCollectTime(): 
    now = current()
    next5min = now + datetime.timedelta(minutes=5)
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
