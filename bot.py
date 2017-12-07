from secrets import *

import tweepy
import json
import haikubot

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

class MyStreamer(tweepy.StreamListener):
    def __init__(self):
        print "Init"

    def on_connect(self):
        print "Connected"

    def on_disconnect(self, status):
        print "Disconnected"

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def on_data(self, data):
        decoded = json.loads(data)
        if decoded.has_key('direct_message'):
            dm = decoded['direct_message']
            dm_text = dm['text']
            dm_sender = dm['sender_screen_name']
            if dm_sender != 'hai_cudi':
                print dm_sender,'asks for',dm_text
                haiku = haikubot.make_haiku(dm_text)
                api.send_direct_message(screen_name=dm_sender,text=haiku)
    

if __name__ == '__main__':
    myStreamListener = MyStreamer()
    stream = tweepy.Stream(auth, myStreamListener)
    stream.userstream()