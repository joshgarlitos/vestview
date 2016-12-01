""" Use this script to insert dummy tweets into Apple MongoDB collection """

import time
import json
from pymongo import MongoClient
from datetime import *
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
import os
import io
from bson import Binary, Code
from bson.json_util import dumps, loads

def _init_(self, start_time):
    self.time = start_time
    self.tweet_data = []

client = MongoClient('localhost', 27017)
db = client['twitter']
sid = SentimentIntensityAnalyzer()
collection = db['Apple']

tweets = ["@APPL stocks down! BUY BUY BUY!",
         "Should I buy @APPL stocks? Give me your guys opinions",
         "I just lost $1.17 per stock @APPL you suck",
         "Who has stocks in @APPL? IF you do, you are an idiot!!!! HAHAHA",
         "I wonder when @APPL is gunna release a new product #waiting#gimme",
         "@APPL not looking good #APPLisdown",
         "LOL my @APPL iPhone already broke -- the worst product ever #dontbuyapple #sad #offthegrid",
         "I cant figure out how this shitty @APPL phone works!!!!!",
         "@APPL users enjoy a phone without a plug for your headphones SO DUMB! #stupidideas#androiduser#nomusic",
         "The day I buy an @APPL product is the day pigs fly. I can't stand Apple!",
         "@APPL is overpriced and I am never going to buy their crap!!!",
         "They are building an @APPL store next to my house, so excited #blessed#lit",
         "Should I buy an @APPL laptop or a PC",
         "@APPL is awesome"]

usernames = ["FinanceMan500", "waveRiderDude", "karen1738", "avidAndroidUser", "dianePrincess1993",
            "mememaster420", "codinggod1337", "1Dfangurl", "seminole4life", "ShasheenIshmal",
            "PunkSk8r", "giraffelover56", "jojo9876", "thorsrighthandman"]

i = 15
for t,u in zip(tweets, usernames):
    date = datetime.now() - timedelta(days=i-1, hours = 0.5*i, minutes = 1.5*i)
    dt = "2016-" + date.strftime("%m") + "-" + date.strftime("%d") + "T22:06:41Z"
    tweet_to_store = {}
    tweet_text = t
    tweet_to_store['text'] = tweet_text
    tweet_to_store['created_at'] = dt;
    tweet_to_store['screen_name'] = u
    tweet_to_store['seniment_score'] = sid.polarity_scores(tweet_text)['compound']
    i = i - 1
    collection.insert(tweet_to_store)