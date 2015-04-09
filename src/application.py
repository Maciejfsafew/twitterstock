from flask import Flask
import os
import time
import yql
import tweepy
from multiprocessing import Process


TWITTER_CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY"]
TWITTER_CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET"]
TWITTER_ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
TWITTER_ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

YAHOO_API_KEY = os.environ["YAHOO_API_KEY"]
YAHOO_SHARED_SECRET = os.environ["YAHOO_SHARED_SECRET"]

app = Flask(__name__)

SYMBOLS = ["YHOO", "AAPL", "GOOG","MSFT", "AMZN", "ADBE", "BIDU", "FB", "NVDA", "EBAY", "INTC"]

@app.route("/")
def hello():
    return "Hello World!"

def get_stock_data():
    print "Process getting stock data started" 
    
    query = 'select * from yahoo.finance.quotes where symbol in ("YHOO", "AAPL", "GOOG","MSFT", "AMZN", "ADBE", "BIDU", "FB", "NVDA", "EBAY", "INTC")'
    y = yql.TwoLegged(api_key=YAHOO_API_KEY, shared_secret=YAHOO_SHARED_SECRET)
    
    while True:
        r = y.execute(query, env="store://datatables.org/alltableswithkeys")
        results = []
        quote = r.results
        if quote:
            for symbol in quote['quote']:
                results.append([symbol['Symbol'], symbol['Ask'], symbol['Volume'], symbol['LastTradeTime'], symbol['LastTradeDate']])
        print results
        results = []
        time.sleep(10)
        
def get_twitter_data():
    print "Process getting twitter data started"


if __name__ == "__main__":
    yahoo = Process(target=get_stock_data)
    yahoo.start()

    twitter = Process(target=get_twitter_data)
    twitter.start()
    
    app.run(host= '0.0.0.0')
