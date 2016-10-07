from flask import Flask, render_template, jsonify
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from collections import OrderedDict
import pandas as pd
from pandas.io.json import json_normalize
import sys
import flask
sys.path.append('../lib')
from yfinance import *
from ymongo import *

app = Flask(__name__)

@app.route('/')
def root():
  """
  This will serve the homepage template
  """
  return render_template("index.html")
  

@app.route("/stock/<symbol>")
def graph(symbol):
  """
  This function essentialy serves the page for http://vestview.com/stock/<SYMBOL>

  TODO: Add multiple stock functionality, make graph more interactive, and update
  graph.html template
  """
  ym = YMongo("vestview", "stocks")
  #returns JSON obj
  stock_data = ym.get_stock(symbol)
  #now normalize the JSON obj to put into pandas dataframe
  df = json_normalize(stock_data)
  #now convert the "data" column to datetime and set it as the index
  df['date'] = pd.to_datetime(df['date'])

  fig = figure(x_axis_type="datetime")
  fig.title = "Stock Closing Prices"
  fig.grid.grid_line_alpha=0.3
  fig.xaxis.axis_label = 'Date'
  fig.yaxis.axis_label = 'Price'
  fig.line(df['date'], df['values.close'], color='#A6CEE3', legend=symbol)
  

  script, div = components(fig)

  return render_template("graph.html", div=div, script=script)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)

