from secrets import *

import tweepy
import re
from textblob import TextBlob
from datetime import datetime

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

class MyStreamer(tweepy.StreamListener):
    def on_status(self, status):
        if status.retweeted:
            return
        text = cleanTweet(status.text)
        print text
        blob = TextBlob(text)

    def on_error(self, status_code):
        if status_code == 420:
            return False


def cleanTweet(tweet):
        # Remove Links, Special Characters etc from tweet
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())


if __name__ == '__main__':
    myStreamListener = MyStreamer()
    stream = tweepy.Stream(auth, myStreamListener)
    stream.filter(track=['Canada', '@JustinTrudeau', 'Toronto'], async=True)
