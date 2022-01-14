from datetime import datetime
from util.logger import logger
import requests
import json

def parse(ticker, API_KEY, quoteTime = datetime.utcnow()):
    interval = 5 # every 5 minutes
    toTime = int(quoteTime.timestamp())
    fromTime = toTime - 60 * interval + 1
    quote_url = f"https://finnhub.io/api/v1/stock/candle?symbol={ticker}&resolution={interval}&from={fromTime}&to={toTime}&token={API_KEY}"
    logger.info(quote_url)

    with requests.Session() as s:
        download = s.get(quote_url)
        decoded_content = download.content.decode('utf-8')
        logger.info(decoded_content)
        quote = json.loads(decoded_content)
        if quote['s'] == 'ok':
            return quote


if __name__ == "__main__":
    toTime = datetime(2022,1,13,13,0,0,0)
    print(int(toTime.timestamp()))
    parse('AAPL', 'c7ce9oqad3idhma69mog', toTime)   