import properties
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import database_manager

symbols = None

class Listener(StreamListener):
    def on_data(self, data):
        parse_tweet(data)
        return True

    def on_error(self, status_code):
        print status_code


def parse_tweet(json_tweet):
    tweet = json.loads(json_tweet)
    if tweet.get('text') is not None:
        tweet_text = tweet['text']
        companies_symbols = get_companies(tweet_text)
        for company_symbol in companies_symbols:
            database_manager.insert_tweet(company_symbol, tweet_text)


def get_companies(tweet):
    companies = []
    for keyword in KEYWORDS:
        if keyword in tweet.upper():
            companies.append(keyword[1:])
    return companies


def read_tags():
    global symbols
    with open("../stocks_list") as symbols_file:
        lines = symbols_file.readlines()
    lines = [line.strip('\n') for line in lines]
    pairs = map(lambda x: x.split("\t"), lines)
    symbols = []
    for pair in pairs:
        database_manager.insert_company(pair[0], pair[1])
        symbols.append(pair[0])
    hashtags = map(lambda x: "#" + x, symbols)
    dollars = map(lambda x: "$" + x, symbols)
    return hashtags + dollars


def start_listening():

    auth = OAuthHandler(properties.twitter_key, properties.twitter_secret)
    auth.set_access_token(properties.twitter_access_token, properties.twitter_access_token_secret)

    twitter_stream = Stream(auth, Listener())
    twitter_stream.filter(track=KEYWORDS)

KEYWORDS = read_tags()