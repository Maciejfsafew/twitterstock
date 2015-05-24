import properties
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

class listener(StreamListener):
    def on_data(self, data):
        print data
        return True
    def on_error(self, status_code):
        print status_code

def read_tags():
    with open("../symbol_list") as symbols_file:
        symbols = symbols_file.readlines()
    symbols = [symbol.strip('\n') for symbol in symbols]
    return symbols

def start_listening():
    SYMBOLS = read_tags()

    auth = OAuthHandler(properties.twitter_key, properties.twitter_secret)
    auth.set_access_token(properties.twitter_access_token, properties.twitter_access_token_secret)

    twitterStream = Stream(auth, listener())
    twitterStream.filter(track=SYMBOLS)