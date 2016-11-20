""" Stream data from Twitter
Requires a local copy of keys.py that is not in Github because
it has private access keys.
"""


import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from keys import *
from pymongo import MongoClient
import io
import os
import json

#Listener Class Override
class listener(StreamListener):

	def __init__(self, start_time):

		self.time = start_time
		self.tweet_data = []

	def on_data(self, data):
		saveFile = io.open('raw_tweets.json', 'a', encoding='utf-8')
		while (time.time() - self.time) < self.limit:
			try:
				tweet = json.loads(data)
				if not tweet['text'].startswith('RT'): #remove retweets
					client = MongoClient('localhost', 27017)
					db = client['twitter_db']
					collection = db['twitter_collection']
					collection.insert(tweet)
				return True
			except BaseException as e:
				print ('failed ondata,', str(e))
				time.sleep(5)
				pass
		exit()


	def on_error(self, status):

		print(status)

	def on_disconnect(self, notice):

		print('bye')



#Beginning of the specific code
start_time = time.time() #grabs the system time

DJIA_STOCKS = [
    "MMM", "AXP", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DIS",
    "DD", "XOM", "GE", "GS", "HD", "IBM", "INTC", "JNJ", "JPM",
    "MCD", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV", "UTX", "UNH",
    "VZ", "V", "WMT"
]

keyword_list = ['@3MInteractive', '@AmericanExpress', '@Apple',
				'@Boeing', '@CaterpillarInc', '@Chevron', '@Cisco',
				'@CocaCola', '@Disney', '@DuPont_News', '@ExxonMobil',
				'@GeneralElectric', '@GoldmanSachs', '@HomeDepot', '@IBM',
				'@Intel', '@JNJCares', '@JPMorgan', '@McDonalds',
				'@Merck', '@Microsoft', '@Nike', '@Pfizer', '@ProcterGamble',
				'@Travelers', '@UTC', '@myUHC', '@Verizon', '@Visa',
				'@Walmart']



auth = OAuthHandler(consumer_key, consumer_secret) #OAuth object
auth.set_access_token(access_token, access_secret)


twitterStream = Stream(auth, listener(start_time)) #initialize Stream object with a time out limit
twitterStream.filter(track=keyword_list, languages=['en'])  #call the filter method to run the Stream Listener