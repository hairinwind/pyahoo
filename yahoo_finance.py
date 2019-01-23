from lxml import html  
import requests
from time import sleep
import json
import argparse
from collections import OrderedDict
from time import sleep
from datetime import datetime
import urllib3
import re

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
	parser = html.fromstring(response.text)
	summary_table = parser.xpath('//div[contains(@data-test,"summary-table")]//tr')
	summary_data = OrderedDict()

	# with open("quote.html", "w", encoding='utf-8') as text_file:
	# 	text_file.write(response.text)

	lastPrice = getFirstItem(parser.xpath("//div[@id='quote-header-info']//span[@data-reactid=14]/text()"))
	afterHourPrice = getFirstItem(parser.xpath("//div[@id='quote-header-info']//span[@data-reactid=20]/text()"))
	afterHourPriceDiff = getFirstItem(parser.xpath("//div[@id='quote-header-info']//span[@data-reactid=23]/text()"))

	try:
		for table_data in summary_table:
			raw_table_key = table_data.xpath('.//td[contains(@class,"C(black)")]//text()')
			raw_table_value = table_data.xpath('.//td[contains(@class,"Ta(end)")]//text()')
			table_key = ''.join(raw_table_key).strip()
			table_value = ''.join(raw_table_value).strip()
			summary_data.update({table_key:table_value})
		summary_data.update({'price':lastPrice, 'ticker':ticker, 'time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
								'afterHourPrice':afterHourPrice, 'afterHourPriceDiff':afterHourPriceDiff
		}) 
		# summary_data.update({'1y Target Est':y_Target_Est,'EPS (TTM)':eps,'Earnings Date':earnings_date,'ticker':ticker,'url':url})
		# print('summary_data', summary_data)
		return summary_data
	except Exception as e:
		print ("Failed to parse json response", e)
		return {"error":"Failed to parse json response"}

def get_cookie_value(r):
    # return {'B': r.cookies['B']}
    return r.cookies.get_dict(domain='.yahoo.com')

def split_crumb_store(v):
    return v.split(':')[2].strip('"')

def find_crumb_store(lines):
    # Looking for
    # ,"CrumbStore":{"crumb":"9q.A4D1c.b9
    for l in lines:
        if re.findall(r'CrumbStore', l):
            return l
    print("Did not find CrumbStore")

def get_page_data(symbol):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    url = "https://finance.yahoo.com/quote/%s/?p=%s" % (symbol, symbol)
    print("quote URL:", url)
    r = requests.get(url, headers=headers)
    print(r.cookies.get_dict(domain='.yahoo.com'))
    cookie = get_cookie_value(r)
    # lines = r.text.encode('utf-8').strip().replace('}', '\n')
    lines = r.content.strip().decode("utf-8").replace('}', '\n')
    return cookie, lines.split('\n')


def get_cookie_crumb(symbol):
    cookie, lines = get_page_data(symbol)
    crumb = split_crumb_store(find_crumb_store(lines))
    # Note: possible \u002F value
    # ,"CrumbStore":{"crumb":"FWP\u002F5EFll3U"
    # FWP\u002F5EFll3U
    # crumb2 = crumb.decode('unicode-escape')
    return cookie, crumb

def sendQuoteRequest(ticker, retry): 
	cookie, crumb = get_cookie_crumb(ticker)
	for i in range(retry):
		url = "http://finance.yahoo.com/quote/%s?p=%s&crumb=%s" % (ticker,ticker,crumb)
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		response = requests.get(url, headers=headers, cookies=cookie, verify=False)
		# print ("Parsing %s"%(url))
		sleep(4)
		if response.status_code == 200:
			return response
		else: 
			print(ticker, response.status_code)
	print('retry time', i)
	return None

def getFirstItem(list):
	return next(iter(list), None)
		
if __name__=="__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument('ticker',help = '')
	args = argparser.parse_args()
	ticker = args.ticker
	print ("Fetching data for %s"%(ticker))
	scraped_data = parse(ticker)
	# print ("Writing data to output file")
	# with open('%s-summary.json'%(ticker),'w') as fp:
	# 	json.dump(scraped_data,fp,indent = 4)