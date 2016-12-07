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

tweets = ["Today I ended a long decline in my relationship with @apple which started 22 years ago. They are completely out of touch with users.",
         ".@Apple @AppleSupport iPhone 7: charging while using headphones, hope you're workin on a solution to do both at the same time. Seriously. MV",
         "I love apple - the iPhone 7 is by far the worst piece of technology I've ever owned, do not buy one. @Apple @AppleSupport",
         "I noticed @Apple iphones are way better then @SamsungMobile phones during cold weather, the touch screen and battery life",
         ".@Apple has removed Brietbart-fake-and-hate-filled-so-called-news from it's app store.  Thank you Apple! ",
         "You can always count on @AppleSupport @Apple to answer the questions you really need answered #NotElite @BarstoolBigCat @PFTCommenter",
         "Going to gather a list of companies that are Anti Conservative for a Boycott by conservatives companies like @Pepsi @Apple @Starbucks",
         "When you call @Apple support and the guy on the phone thanks you for being the nicest person he's talked to all day. #ImCanadian",
         "I need a new phone. Is the iPhone 7 worth getting? I hate that it doesn't have a plugin for my head phones. @Apple",
         "For the life of me, I can't figure out why iPhone autocorrects 'deadlift' to 'deadliest'. Guess nobody at @Apple lifts. So ducking annoying.",
         "Thank you @Apple for making your #iPhone7 with amazing battery life. I haven't charged it for 24 hrs and it's still going strong.",
         "First extremely inconvenient experience with the iPhone 7 is trying to watch Netflix on my phone but also needing a charge @Apple",
         "Loving My iPad & Apple Watch. I've Stepped My @Apple Game Up!!",
         "Still waiting for @Apple to not autocorrect haha to Gaga every time I mishit the buttons",
         "I love my iPhone 5S ! @Apple",
         "Bad customer service @Apple   Wife had battery issues, made appt week ago now told 1-2 weeks for repair.",
         "Please @apple, can you sort out the usability disaster that is Apple Music? Thanks from millions of users.",
         "Just got the 7 yesterday and it's messing up already. @Apple @AppleSupport wyd? Get it together.",
         "Yeah I update my phone as soon as I update it within a week it's fucked no sound keeps going off @Apple are you taking the piss",
         "Ok @Apple where is the mermaid emoji",
         "dear @AppleSupport @Apple can you please remove that #presshometoenter on my phone #update IT IS STUPID",
         "Hey @Apple, where's our tattoo gun emoji at??",
         "YOUR PRODUCTS ARE THE WORST @Apple",
         ]

usernames = ["DaveMcKean", "MiloVentimiglia", "NoteBloom",
            "fdamusic", "@PaladinCornelia", "JGRAD99", "Brian_Was_Here_", "JordanMcIntosh",
            "ScottWarner18", "benbruno1", "m0rganrebecca", "casssieyoung", "ItsMamazBoi",
            "awood24",
            "darklushlash",
            "robertjlederman",
            "g_e_r_b",
            "_AutumnSays",
            "kylerazwan",
            "charlielawlor17",
            "TanteKee",
            "haylzno",
            "maliasgilinsky"]

dates = [1479213240, 1479299640, 1479386040, 1479472440, 1479558840, 1479645240, 1479731640, 1479818040, 
        1479904440, 1479990840, 1480077240, 1480163640, 1480250040, 1480336440, 1480422840, 1480509240,
        1480595640, 1480682040, 1480768440, 1480854840, 1480941240, 1480941240, 1480941240]


i = 23
for t,u,d in zip(tweets, usernames, dates):
    tweet_to_store = {}
    tweet_text = t
    tweet_to_store['text'] = tweet_text
    tweet_to_store['created_at'] = d;
    tweet_to_store['screen_name'] = u
    tweet_to_store['sentiment_score'] = sid.polarity_scores(tweet_text)['compound']
    i = i - 1
    collection.insert(tweet_to_store)