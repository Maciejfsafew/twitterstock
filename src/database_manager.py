from psycopg2 import connect
import datetime

con = None
con = connect(dbname="twitterstock", user="postgres", host="localhost", password="admin")

cur = con.cursor()


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
    cur.execute('SELECT company_id FROM "Companies" WHERE company_symbol = %s', (company_symbol,))
    company_id = cur.fetchone()[0]
    cur.execute('INSERT INTO "Tweets"(company_id, time, text) VALUES(%s, %s, %s)',
                (company_id, datetime.datetime.now(), tweet_text))
    con.commit()


def close_connection():
    cur.close()
    con.close()