from flask import Flask
from flask import render_template
from flask import request
import time
from multiprocessing import Process
from yahoo_finance import Share
import twitter_manager
import datetime
import database_manager

app = Flask(__name__)
app.config.update(
    PROPAGATE_EXCEPTIONS=True
)

SYMBOLS = []
def init():
    with open("../symbol_list") as symbols_file:
        symbols = symbols_file.readlines()
    for symbol in symbols:
        SYMBOLS.append(symbol.strip('\r\n'))

SYMBOL = "YHOO"

@app.route("/", methods=['POST', 'GET'])
def hello():
    if not len(SYMBOLS):
        init()
        print SYMBOLS
    SB = SYMBOL    
    if request.method == 'POST':
        sym = request.form['symbol']
        if sym in SYMBOLS:
            SB = sym
    symbol = Share(SB)
    data = symbol.get_historical('2015-01-01', time.strftime("%Y-%m-%d", time.gmtime()))
    DATA=[]
    METRICS=[]
    avg = 0.0
    var = 0.0
    for row in data:
        high = float(row['High'])
        ope = float(row['Open'])
        low = float(row['Low'])
        close = float(row['Close'])
        avg = 0.75 * avg + 0.25 * close 
        var = 0.75 * var + 0.25 * abs(high - low)
        DATA.append([row['Date'], row['Low'], row['Open'], row['Close'], row['High']])
        METRICS.append([row['Date'], str(avg), str(var)])
    return render_template('main_view.html', symbols=SYMBOLS, data=DATA, symbol=SB, metrics=METRICS)


@app.route("/tweets", methods=['POST', 'GET'])
def show_tweets():
    if not len(SYMBOLS):
        init()
        print SYMBOLS
    SB = "AAPL"
    start_date = datetime.datetime(2015, 5, 26, 22)
    end_date = datetime.datetime(2015, 5, 27)
    DATE = ""
    if request.method == 'POST':
        sym = request.form['symbol']
        if sym in SYMBOLS:
            SB = sym
        DATE = request.form['date']
        if DATE != "":
            date_values = map(lambda x: int(x), DATE.split("/"))
            start_date = datetime.datetime(date_values[2], date_values[0], date_values[1], 14, 30)
            end_date = datetime.datetime(date_values[2], date_values[0], date_values[1], 22)
    COMPANY_NAME = database_manager.get_company_name(SB)
    DATA = twitter_manager.get_tweets_in_periods(SB, start_date, end_date)
    print DATA
    return render_template('tweet_view.html', symbols=SYMBOLS, data=DATA, symbol=SB, company_name=COMPANY_NAME,
                           date=DATE)

def get_twitter_data():
    print "Process getting twitter data started"
    twitter_manager.start_listening()

if __name__ == "__main__":
    twitter = Process(target=get_twitter_data)
    twitter.start()
    
    app.run(host= '0.0.0.0')
