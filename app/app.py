from flask import Flask, render_template, jsonify
import sys
import flask
sys.path.append('../lib')
from yfinance import *
from ymongo import *

app = Flask(__name__)

DJIA = ["MMM", "AXP", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DIS",
        "DD", "XOM", "GE", "GS", "HD", "IBM", "INTC", "JNJ", "JPM",
        "MCD", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV", "UTX", "UNH",
        "VZ", "V", "WMT"]

"""
This will serve the homepage template
"""
@app.route('/')
def root():

  return render_template("index.html")

"""
This is the interactive chart page for a specific stock
"""
@app.route('/chart/<symbol>')
def chart(symbol):
  return render_template("chart.html", symbol=symbol)

"""
This is matt's page, index.html search directs to /chart/<symbol>, but if you
want to test this page just go directly to /graph/<symbol>
"""

@app.route('/graph/<symbol>')
def graph(symbol):
  company = "Apple Inc."
  return render_template("graph.html", symbol=symbol, company=company)

"""
This page returns historical data for a specific stock
* this page is simply used for data
"""
@app.route("/data/<symbol>")
def data(symbol):
  ym = YMongo("vestview", "stocks")
  stock_data = ym.get_stock(symbol)
  return json.dumps(stock_data)

"""
This page returns current data for ALL DJIA stocks
* this page is simply used for data
"""
@app.route("/djia")
def all_djia_stocks():
  yf = YFinance()
  # returns array of JSON objs with all DJIA stock prices
  stock_data = yf.get_quote(DJIA)
  return json.dumps(stock_data)



if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)
