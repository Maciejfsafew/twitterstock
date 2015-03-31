import yql
import os
y = yql.TwoLegged(api_key=os.environ["API_KEY"], shared_secret=os.environ["SHARED_SECRET"])

query = 'select * from yahoo.finance.quotes where symbol in ("YHOO", "AAPL", "GOOG","MSFT", "AMZN", "ADBE", "BIDU", "FB", "NVDA", "EBAY", "INTC")';

r = y.execute(query, env="store://datatables.org/alltableswithkeys")

print r.results
