from bs4 import BeautifulSoup
from collections import OrderedDict
from datetime import datetime
# from lxml import html 
from os import environ
from time import sleep
from util import dateUtil
import argparse
import json
import re
import requests
import urllib3
import sys

# if environ.get('PYTHON_ENV') != 'prod':
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def parse(ticker, retry=10):
    response = sendQuoteRequest(ticker, retry)
    if response == None:
        print()
        print('did not get quote', ticker, datetime.utcnow())
        print()
        return None
    else: 
        return parseResponse(ticker, response)

def parseResponse(ticker, response):
    soup = BeautifulSoup(response.text, 'html5lib')
    scriptsFound = soup.body.find_all('script')
    appMainScripts = [x.text for x in scriptsFound if x.string is not None and 'root.App.main' in x.text]
    regex = r"root.App.main.*;"
    matches = re.search(regex, appMainScripts[0])
    appMainText = matches.group(0)
    # appMainText is root.App.main = {...json...}; I only need the json part
    appMainText1 = appMainText[appMainText.index('{'):]
    if appMainText1.endswith(';'):
        appMainText1 = appMainText1[:len(appMainText1)-1]
    
    appMain = json.loads(appMainText1)    
    priceSection =  appMain['context']['dispatcher']['stores']['QuoteSummaryStore']['price']
    nowStr = datetime.now().strftime("%Y-%m-%d %H:%M")
    summary = OrderedDict()
    summary.update({'symbol': ticker, 'currentTime': nowStr})   
    summary.update(appMain['context']['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail'])

    summary = summaryUpdate(summary, priceSection, 
        ['regularMarketChange', 'regularMarketPrice', 'regularMarketChangePercent', 'regularMarketTime',
        'postMarketTime', 'postMarketPrice', 'postMarketChange', 'preMarketChangePercent',
        'preMarketTime','preMarketPrice', 'preMarketChange', 'postMarketChangePercent'
        ])
    return summary

def summaryUpdate(summary, priceSection, priceSectionProps):
    for prop in priceSectionProps:
        value = priceSection.get(prop, None)
        summary.update({prop: value})
    return summary

# def parseResponse(ticker, response):
#     parser = html.fromstring(response.text)
#     summary_table = parser.xpath('//div[contains(@data-test,"summary-table")]//tr')
#     summary_data = OrderedDict()

#     # if datetime.now().hour == 8:
#     #     nowStr = datetime.now().strftime("%Y%m%d%H%M")
#     #     with open(ticker + "_" +nowStr+ ".html", "w", encoding='utf-8') as text_file:
#     #         text_file.write(response.text)
    
#     # lastPrice = getFirstItem(parser.xpath("//div[@id='quote-header-info']//span[@data-reactid=14]/text()"))
#     # afterHourPrice = getFirstItem(parser.xpath("//div[@id='quote-header-info']//span[@data-reactid=20]/text()"))
#     # afterHourPriceDiff = getFirstItem(parser.xpath("//div[@id='quote-header-info']//span[@data-reactid=23]/text()"))
#     lastPrice, afterHourPrice, afterHourPriceDiff, afterHourPercent, beforeHourPrice, beforeHourPriceDiff, beforeHourPercent = getPrice(ticker, response)

#     try:
#         for table_data in summary_table:
#             raw_table_key = table_data.xpath('.//td[contains(@class,"C(black)")]//text()')
#             raw_table_value = table_data.xpath('.//td[contains(@class,"Ta(end)")]//text()')
#             table_key = ''.join(raw_table_key).strip()
#             table_value = ''.join(raw_table_value).strip()
#             summary_data.update({'ticker':ticker, 'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'price':lastPrice})
#             if dateUtil.isPreMarket():
#                 summary_data.update({'beforeHourPrice':beforeHourPrice, 'beforeHourPriceDiff':beforeHourPriceDiff, 'beforeHourPercent': beforeHourPercent})
#             if dateUtil.isPostMarket(): 
#                 summary_data.update({'afterHourPrice':afterHourPrice, 'afterHourPriceDiff':afterHourPriceDiff, 'afterHourPercent': afterHourPercent})
#             summary_data.update({table_key:table_value})
#         # summary_data.update({'1y Target Est':y_Target_Est,'EPS (TTM)':eps,'Earnings Date':earnings_date,'ticker':ticker,'url':url})
#         # print('summary_data', summary_data)
#         return summary_data
#     except Exception as e:
#         print ("Failed to parse json response", e)
#         return {"error":"Failed to parse json response"}

# def getPrice(ticker, response): 
#     soup = BeautifulSoup(response.text, 'html5lib')
#     scriptsFound = soup.body.find_all('script')
#     appMainScripts = [x.text for x in scriptsFound if x.string is not None and 'root.App.main' in x.text]
#     regex = r"root.App.main.*;"
#     matches = re.search(regex, appMainScripts[0])
#     appMainText = matches.group(0)
#     # appMainText is root.App.main = {...json...}; I only need the json part
#     appMainText1 = appMainText[appMainText.index('{'):]
#     if appMainText1.endswith(';'):
#         appMainText1 = appMainText1[:len(appMainText1)-1]
    
#     appMain = json.loads(appMainText1)
#     priceSection =  appMain['context']['dispatcher']['stores']['QuoteSummaryStore']['price']
#     lastPrice = float(priceSection['regularMarketPrice']['fmt'].replace(',',''))
#     afterHourPrice = float(priceSection['postMarketPrice']['fmt'].replace(',','')) if priceSection['postMarketPrice'] else None
#     afterHourPriceDiff = float(priceSection['postMarketChange']['fmt'].replace(',','')) if priceSection['postMarketChange'] else None
#     afterHourPercent = priceSection['postMarketChangePercent']['fmt'] if priceSection.get('postMarketChangePercent', None) else None
#     beforeHourPrice = float(priceSection['preMarketPrice']['fmt'].replace(',','')) if priceSection['preMarketPrice'] else None
#     beforeHourPriceDiff = float(priceSection['preMarketChange']['fmt'].replace(',','')) if priceSection['preMarketChange'] else None
#     beforeHourPercent = priceSection['preMarketChangePercent']['fmt'] if priceSection.get('preMarketChangePercent', None) else None

#     return lastPrice, afterHourPrice, afterHourPriceDiff, afterHourPercent, beforeHourPrice, beforeHourPriceDiff, beforeHourPercent

def sendQuoteRequest(ticker, retry): 
    for i in range(retry):
        url = "http://finance.yahoo.com/quote/%s?p=%s"%(ticker,ticker)
        response = requests.get(url, verify=False)
        # print ("Parsing %s"%(url))
        sleep(4)
        if response.status_code == 200:
            return response
    print('retry time', i)
    return None

def getFirstItem(list):
    return next(iter(list), None)

def test():
    from symbol import readSymbolsFromFile
    symbols = readSymbolsFromFile()
    for symbol in symbols:
        parse(symbol, retry=1)
        print('collect quote for %s' % symbol)
        
if __name__=="__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('ticker',help = '')
    args = argparser.parse_args()
    ticker = args.ticker
    print ("Fetching data for %s"%(ticker))
    scraped_data = parse(ticker)
    print(scraped_data)

    # print ("Writing data to output file")
    # with open('%s-summary.json'%(ticker),'w') as fp:
    #     json.dump(scraped_data,fp,indent = 4)

    # test()