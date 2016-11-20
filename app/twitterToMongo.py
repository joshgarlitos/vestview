""" Pulls data from Twitter and stores in MongoDB
"""

# tweepy setup
import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from keys import *
from pymongo import MongoClient
import io
import os
import json

class listener(StreamListener):
	""" Overriding Tweepy Listener class Listener streaming should never end """

	def __init__(self, start_time):
		self.time = start_time
		self.tweet_data = []

	def on_data(self, data):
		""" Takes data and puts into json. Filters by company and stores
		in collection named after the specific company """
		try:
			tweet = json.loads(data)
			if not tweet['text'].startswith('RT'): #remove retweets
				for company in keyword_list:
					if company.lower() in tweet['text'].lower(): # Check tweet text for @company
						client = MongoClient('localhost', 27017) # Store it in respective db if there
						db = client['twitter']
						collection = db[company]
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


"""
Running of stream listener:
"""
start_time = time.time() #grabs the system time

# Store all the companies by twitter handle
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

# Start the stream listener
twitterStream = Stream(auth, listener(start_time)) #initialize Stream object with a time out limit
twitterStream.filter(track=keyword_list, languages=['en'])  #call the filter method to run the Stream Listener
