import tweepy
import os

TWITTER_CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY"]
TWITTER_CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET"]
TWITTER_ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
TWITTER_ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)

auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
public_tweets = api.home_timeline()

for tweet in public_tweets:
    print tweet
