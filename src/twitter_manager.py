import properties
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

SYMBOLS = ["YHOO", "AAPL", "GOOG", "MSFT", "AMZN", "ADBE", "BIDU", "FB", "NVDA", "EBAY", "INTC"]

class listener(StreamListener):
    def on_data(self, data):
        print data
        return True
    def on_error(self, status_code):
        print status_code

def start_listening():
    auth = OAuthHandler(properties.twitter_key, properties.twitter_secret)
    auth.set_access_token(properties.twitter_access_token, properties.twitter_access_token_secret)

    twitterStream = Stream(auth, listener())
    twitterStream.filter(track=SYMBOLS)