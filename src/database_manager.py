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

cur = con.cursor()
cur_read = con_read.cursor()

def get_company_id(company_symbol):
    cur_read.execute('SELECT company_id FROM "Companies" WHERE company_symbol = %s', (company_symbol,))
    return cur_read.fetchone()[0]

def insert_company(company_symbol, company_name):
    """
    Inserts into DB company info if that company does not exist already.
    :param company_symbol: Company symbol, e.g. MSFT
    :param company_name: Company name, e.g. Microsoft
    """
    cur.execute(
        '''INSERT INTO "Companies"(company_symbol, company_name)
            SELECT %s, %s WHERE NOT EXISTS (SELECT * FROM "Companies" WHERE company_symbol = %s)''',
        (company_symbol, company_name, company_symbol))
    con.commit()


def insert_tweet(company_symbol, tweet_text):
    """
    Inserts into DB tweet.
    :param company_symbol: Symbol of company which of tweet is saying
    :param tweet_text: content of tweet
    """
    company_id = get_company_id(company_symbol)
    cur.execute('INSERT INTO "Tweets"(company_id, time, text) VALUES(%s, %s, %s)',
                (company_id, datetime.datetime.now(), tweet_text))
    con.commit()


def get_tweets_for_company(company_symbol, start_date, end_date):
    company_id = get_company_id(company_symbol)
    cur_read.execute('SELECT * FROM "Tweets" WHERE company_id = %s AND time BETWEEN %s AND %s',
                (company_id, start_date, end_date))
    return cur_read.fetchall()


def get_company_name(company_symbol):
    cur_read.execute('SELECT company_name FROM "Companies" WHERE company_symbol = %s', (company_symbol,))
    return cur_read.fetchone()[0]


def close_connection():
    cur.close()
    con.close()
