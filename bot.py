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
        exclusion_list = ['938597347046580224', 'haikus420']
        decoded = json.loads(data)
        if decoded.has_key('direct_message'):
            dm = decoded['direct_message']
            dm_sender_id = dm['sender_id_str']
            dm_text = dm['text']
            dm_sender = dm['sender_screen_name']
            if dm_sender != 'hai_cudi':
                if dm_sender_id in exclusion_list or dm_sender in exclusion_list:
                    text = 'Sorry. No haiku or lyrics found.'
                    api.send_direct_message(screen_name=dm_sender, text=text)
                else:
                    print dm_sender, 'asks for', dm_text
                    haiku = haikubot.make_haiku(dm_text)
                    api.send_direct_message(screen_name=dm_sender, text=haiku)
                    
    

if __name__ == '__main__':
    with open('all_dms.txt','w') as out:
        dms = api.direct_messages()
        for dm in dms:
            out.write(str(dm))
    myStreamListener = MyStreamer()
    stream = tweepy.Stream(auth, myStreamListener)
    stream.userstream()
