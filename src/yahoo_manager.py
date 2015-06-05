from psycopg2 import connect
from yahoo_finance import Share
import datetime
import properties
import application
import time

con = connect(dbname=properties.db_name,
              user=properties.db_username,
              host=properties.db_host,
              password=properties.db_password)
con_read = connect(dbname=properties.db_name,
              user=properties.db_username,
              host=properties.db_host,
              password=properties.db_password)

def get_company_id(company_symbol):
    cur = con.cursor()
    cur.execute('SELECT company_id FROM "Companies" WHERE company_symbol = %s', (company_symbol,))
    company_id = cur.fetchone()[0]
    cur.close()
    return company_id
    
def insert_financial_data(company_id, price, volume):
    """
    Inserts into DB tweet.
    :param company_symbol: Symbol of company which of tweet is saying
    :param tweet_text: content of tweet
    """
    cur = con.cursor()
    cur.execute('INSERT INTO "Quotes"(company_id, time, volume, ask) VALUES(%s, %s, %s, %s)',
                (company_id, datetime.datetime.now(), volume, price))
    con.commit()
    cur.close()

def start_listening():
    symbols = application.init()
    listeners = []
    for symbol in symbols:
        listeners.append([symbol, Share(symbol), get_company_id(symbol)])
    while True:
        for symbol, share , company_id in listeners:
            share.refresh()
            insert_financial_data(company_id, share.get_price(), share.get_volume())
        time.sleep(30)
