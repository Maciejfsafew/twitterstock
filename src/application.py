from flask import Flask, Blueprint, render_template
# import yql
import tweepy
from multiprocessing import Process
import properties
import chartkick
import time
import datetime
import random

TWITTER_CONSUMER_KEY = properties.twitter_key
TWITTER_CONSUMER_SECRET = properties.twitter_secret
TWITTER_ACCESS_TOKEN = properties.twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET = properties.twitter_access_token_secret

# YAHOO_API_KEY = os.environ["YAHOO_API_KEY"]
# YAHOO_SHARED_SECRET = os.environ["YAHOO_SHARED_SECRET"]

app = Flask(__name__)

ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')
app.register_blueprint(ck, url_prefix='/ck')
app.jinja_env.add_extension("chartkick.ext.charts")

SYMBOLS = ["YHOO", "AAPL", "GOOG","MSFT", "AMZN", "ADBE", "BIDU", "FB", "NVDA", "EBAY", "INTC"]

@app.route("/")
def hello():
    # return "Hello World!"
    return render_template('layout.html', data={'Chrome': 52.9, 'Opera': 1.6, 'Firefox': 27.7})

@app.route("/chart")
def charts_example():
    ts = time.time()
    price = 50.5
    volume = 100000
    data_prices = {}
    data_volume = {}
    for i in range(100):
        ts += 300
        price_diff = (random.random() - 0.5)*5
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        price += price_diff
        volume_diff = (random.random() - 0.5) * 1000
        volume += volume_diff
        data_prices[timestamp] = price
        data_volume[timestamp] = volume
    return render_template('layout.html', data_prices=data_prices, data_volume=data_volume, stock_name="MSFT")

# def get_stock_data():
#     print "Process getting stock data started"
#
#     query = 'select * from yahoo.finance.quotes where symbol in ("YHOO", "AAPL", "GOOG","MSFT", "AMZN", "ADBE", "BIDU", "FB", "NVDA", "EBAY", "INTC")'
#     y = yql.TwoLegged(api_key=YAHOO_API_KEY, shared_secret=YAHOO_SHARED_SECRET)
#
#     while True:
#         r = y.execute(query, env="store://datatables.org/alltableswithkeys")
#         results = []
#         quote = r.results
#         if quote:
#             for symbol in quote['quote']:
#                 results.append([symbol['Symbol'], symbol['Ask'], symbol['Volume'], symbol['LastTradeTime'], symbol['LastTradeDate']])
#         print results
#         results = []
#         time.sleep(10)
        
def get_twitter_data():
    print "Process getting twitter data started"


if __name__ == "__main__":
    # yahoo = Process(target=get_stock_data)
    # yahoo.start()

    twitter = Process(target=get_twitter_data)
    twitter.start()

    app.debug = True
    app.run(host= '0.0.0.0')


