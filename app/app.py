from flask import Flask, render_template, jsonify
from datetime import datetime
import sys
sys.path.append('../lib')
from yfinance import *
from yfmongo import *
from gfnews import *

MONGODB_HOST = "localHost"
DBS_NAME = "vestview"
COLLECTION_NAME = "stocks"


app = Flask(__name__)

@app.route('/')
def root():
	"""
	This will serve the homepage template
	The data JSON obj is sent to the client side for real-time
	autocomplete data
	"""
	DJIA = ["MMM", "AXP", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DIS",
				"DD", "XOM", "GE", "GS", "HD", "IBM", "INTC", "JNJ", "JPM",
				"MCD", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV", "UTX", "UNH",
				"VZ", "V", "WMT"]

	data = get_quote(DJIA)

	return render_template("index.html", autocompleteData=data)

@app.route("/chart/<symbol>")
def graph(symbol):
	"""
	This function essentialy serves the page for http://vestview.com/stock/<SYMBOL>

	TODO: Add multiple stock functionality, make graph more interactive, and update
	graph.html template
	"""
	yfm = YFMongo(DBS_NAME, COLLECTION_NAME)
	daily_data = yfm.get_stock_data(symbol)
	articles = get_news_data(symbol)
	return render_template("chart.html", data=daily_data, articles=articles, symbol=symbol)


@app.route("/graph")
def test():
	return render_template("graph.html")

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)

