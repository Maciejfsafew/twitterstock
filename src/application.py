from flask import Flask
from flask import render_template
from flask import request
import time
from multiprocessing import Process
from yahoo_finance import Share
import twitter_manager

app = Flask(__name__)

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

def get_twitter_data():
    print "Process getting twitter data started"
    twitter_manager.start_listening()

if __name__ == "__main__":
    twitter = Process(target=get_twitter_data)
    twitter.start()
    
    app.run(host= '0.0.0.0')
