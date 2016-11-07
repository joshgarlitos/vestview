from flask import Flask, render_template, jsonify
import sys
sys.path.append('../lib')
from yfinance import *
from ymongo import *

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
  yf = YFinance()

  data = yf.get_quote(DJIA)

  return render_template("index.html", autocompleteData=data)

@app.route("/chart/<symbol>")
def graph(symbol):
  """
  This function essentialy serves the page for http://vestview.com/stock/<SYMBOL>

  TODO: Add multiple stock functionality, make graph more interactive, and update
  graph.html template
  """
  ym = YMongo(DBS_NAME, COLLECTION_NAME)

  #returns JSON obj
  stock_data = ym.get_stock(symbol)

  return render_template("chart.html", data=stock_data)



@app.route("/graph")
def test():
  return render_template("graph.html")

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)

