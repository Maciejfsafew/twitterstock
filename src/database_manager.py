from psycopg2 import connect
import datetime
import properties

con = None
con = connect(dbname=properties.db_name,
              user=properties.db_username,
              host=properties.db_host,
              password=properties.db_password)
con_read = connect(dbname=properties.db_name,
              user=properties.db_username,
              host=properties.db_host,
              password=properties.db_password)

def get_company_id(company_symbol):
    cur = con_read.cursor()
    cur.execute('SELECT company_id FROM "Companies" WHERE company_symbol = %s', (company_symbol,))
    company_id = cur.fetchone()[0]
    cur.close()
    return company_id

def insert_company(company_symbol, company_name):
    """
    Inserts into DB company info if that company does not exist already.
    :param company_symbol: Company symbol, e.g. MSFT
    :param company_name: Company name, e.g. Microsoft
    """
    cur = con.cursor()
    cur.execute(
        '''INSERT INTO "Companies"(company_symbol, company_name)
            SELECT %s, %s WHERE NOT EXISTS (SELECT * FROM "Companies" WHERE company_symbol = %s)''',
        (company_symbol, company_name, company_symbol))
    con.commit()
    cur.close()


def insert_tweet(company_symbol, tweet_text):
    """
    Inserts into DB tweet.
    :param company_symbol: Symbol of company which of tweet is saying
    :param tweet_text: content of tweet
    """
    company_id = get_company_id(company_symbol)
    cur = con.cursor()
    cur.execute('INSERT INTO "Tweets"(company_id, time, text) VALUES(%s, %s, %s)',
                (company_id, datetime.datetime.now(), tweet_text))
    con.commit()
    cur.close()

def get_tweets_for_company(company_symbol, start_date, end_date):
    company_id = get_company_id(company_symbol)
    cur = con_read.cursor()
    cur.execute('SELECT * FROM "Tweets" WHERE company_id = %s AND time BETWEEN %s AND %s',
                (company_id, start_date, end_date))
    tweets = cur.fetchall()
    cur.close()
    return tweets


def get_company_name(company_symbol):
    cur = con_read.cursor()
    cur.execute('SELECT company_name FROM "Companies" WHERE company_symbol = %s', (company_symbol,))
    name = cur.fetchone()[0]
    cur.close()
    return name


def close_connection():
    con.close()
