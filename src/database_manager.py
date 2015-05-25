from psycopg2 import connect

con = None
con = connect(dbname="twitterstock", user="postgres", host="localhost", password="admin")

cur = con.cursor()


def insert_company(company_symbol, company_name):
    """
    Inserts into DB company info if that company does not exist already.
    :param company_symbol: Company symbol, e.g. MSFT
    :param company_name: Company name, e.g. Microsoft
    """
    cur.execute('INSERT INTO "Companies"(company_symbol, company_name) SELECT %s, %s WHERE NOT EXISTS (SELECT * FROM "Companies" WHERE company_symbol = %s)', (company_symbol, company_name, company_symbol))
    con.commit()


def close_connection():
    cur.close()
    con.close()