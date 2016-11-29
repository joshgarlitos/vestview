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
import nltk
nltk.download('punkt') # sentiment analysis
nltk.download('vader_lexicon') # sentiment analysis
from nltk.sentiment import SentimentIntensityAnalyzer
import datetime

class listener(StreamListener):
	""" Overriding Tweepy Listener class. Listener streaming should never end """

	def __init__(self, start_time):
		self.time = start_time
		self.tweet_data = []

	def on_data(self, data):
		""" Takes data and puts into json. Filters by company and stores
		in collection named after the specific company """
		
		# Open MongoDB Connection & SentimentIntensityAnalyzer
		client = MongoClient('localhost', 27017)
		db = client['twitter']
		sid = SentimentIntensityAnalyzer()

		try:
			tweet = json.loads(data) #tweet is a dict
			if "text" in tweet and not tweet['text'].startswith('RT'): #remove retweets
				tweet_text = tweet["text"]
				for company in keyword_list:
					if company.lower() in tweet['text'].lower(): # Check tweet text for @company
						collection = db[company.replace('@','')] # get rid of @ for storing in MongoDB collection

						# Prune data and perform sentiment analysis on tweet
						created_at = tweet['created_at']
						dt = datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y') # convert to Python datatime
						sentiment_scores = sid.polarity_scores(tweet_text)

						# Create tweet to be stored
						tweet_to_store = {}
						tweet_to_store['text'] = tweet['text']
						tweet_to_store['created_at'] = dt # store Python datetime version of created_at
						tweet_to_store['location'] = tweet['user']['location']
						tweet_to_store['screen_name'] = tweet['user']['screen_name']
						tweet_to_store['sentiment_score'] = sentiment_scores['compound']

						# Store the tweet
						collection.insert(tweet_to_store)
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

def getTweets(symbol):
	""" Grabs all tweets stored in MongoDB for company.
	Pass in company stock ticker symbol and return all tweets for that company"""

	# Convert ticker symbol to company collection name in MongoDB
	ticker_Dict = { "MMM" : "3MInteractive", "AXP" : "AmericanExpress" , 
					"AAPL" : "Apple", "BA" : "Boeing" , "CAT" : "CaterpillarInc", "CVX" : "Chevron", 
					"CSCO" : "Cisco", "KO" : "CocaCola", "DIS" : "Disney",
					"DD" : "Dupont_News", "XOM" : "ExxonMobil", "GE" : "GeneralElectric", 
					"GS" : "GoldmanSachs", "HD" : "HomeDepot", "IBM" : "IBM", 
					"INTC" : "Intel", "JNJ" : "JNJCares", "JPM" : "JPMorgan",
					"MCD" : "McDonalds", "MRK" : "Merck", "MSFT" : "Microsoft", 
					"NKE" : "Nike", "PFE" : "Pfizer", "PG" : "ProcterGamble", 
					"TRV" : "Travelers", "UTX" : "UTC", "UNH" : "myUHC",
					"VZ" : "Verizon", "V" : "Visa", "WMT" : "Walmart"}

	client = MongoClient('localhost', 27017)
	db = client['twitter']
	twitter_handle = ticker_Dict.get(symbol, None)
	collection = db[twitter_handle]

	tweets_iterator = collection.find() # gets all tweets in company collection
	tweet_list = []

	""" Creates a list containing a dict for each tweet """ 
	for tweet in tweets_iterator:
		tweet_list.append(tweet)

	return tweet_list


"""
Running of stream listener:
"""
if __name__ == "__main__":
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
