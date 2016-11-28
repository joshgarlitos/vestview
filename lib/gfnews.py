import requests
import json
import demjson
import time
import re
import argparse
from datetime import datetime, date, timedelta
from pymongo import MongoClient

_GOOGLE_NEWS_BASE_URL = "http://www.google.com/finance/company_news?"

_KEYMAP = {
    "a": "articles",
    "d": "date",
    "s": "source",
    "t": "title",
    "tt": "titleId",
    "u": "url",
    "sp": "openingSentence"
}

DJIA_STOCKS = [
    "MMM", "AXP", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DIS",
    "DD", "XOM", "GE", "GS", "HD", "IBM", "INTC", "JNJ", "JPM",
    "MCD", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV", "UTX", "UNH",
    "VZ", "V", "WMT"
]


def _parse_date(date_str):
    """ Turns a date string into a valid datetime object"""
    date_str_regex = re.compile("[\w]{3} [\d]{1,2}, [\d]{4}")
    hours_ago_regex = re.compile("[\d]{1,2} [\w]+ ago")

    if date_str_regex.match(date_str):
        try:
            return datetime.strptime(date_str, "%b %d, %Y")
        except ValueError:
                pass
    elif hours_ago_regex.match(date_str):
        try:
            return datetime.combine(date.today(), datetime.min.time())
        except:
            pass
    raise ValueError("couldn't parse date string: {0}".format(date_str))

def make_keys_verbose(article_dict):
    for old_key in article_dict:
        if old_key in _KEYMAP:
            new_key = _KEYMAP[old_key]
            article_dict[new_key] = article_dict.pop(old_key)


def get_news(symbol, num_articles=500):
    """
    notes on googleFinance news JSONP response
    GoogleFinance clusters articles that have similar content

    It's an array of nested dictionaries corresponding to the clustered articles.
    Each element in the array has
    {
        ....
        "lead_story_url": this is the lead story, aka the theme of the cluster
        "a": [  ....
                {
                    "s": "Motley Fool",
                    "d": "Nov 23, 2016",
                    "sp": "sp": "According to a report....third quarter of 2016.",
                    "t": "Apple Inc.&#39;s Mysterious OLED iPhone Revealed"
                    "u": "'http://www.fool.com/investing/....revealed.aspx"
                }
                ....
            ]
    }
    """
    payload = {
        "output": "json",
        "q": symbol,
        "num": num_articles,
        "start": 0
    }
    json_str = requests.get(_GOOGLE_NEWS_BASE_URL, params=payload).text
    # need demjson's decode, json data is invalid for pythons native decoder
    article_clusters = demjson.decode(json_str)['clusters']

    articles = []
    for cluster in article_clusters:
        if "a" in cluster:
            for article in cluster["a"]:
                make_keys_verbose(article)
                article["date"] = _parse_date(article["date"])
                articles.append(article)

    articles.sort(key=lambda d: d["date"])
    return articles


def insert_djia_news():
        mc = MongoClient("localhost", 27017)
        db = mc["news"]

        for symbol in DJIA_STOCKS:
            coll = db[symbol]
            articles = get_news(symbol, num_articles=500)
            # unique dates for articles
            dates = list({d["date"] for d in articles})
            dates.sort()
            curr_ix = 0
            total_articles_inserted = 0
            for curr_date in dates:
                if not coll.find({"date":curr_date}).count():
                    doc_to_insert = {
                        "date": curr_date,
                        "articles": []
                    }
                    while(curr_ix < len(articles) and articles[curr_ix]["date"] == curr_date):
                        doc_to_insert["articles"].append(articles[curr_ix])
                        curr_ix += 1

                    date_str = curr_date.strftime("%m-%d-%Y")
                    print("Inserting {0} news articles published on {1} for {2}".format(len(doc_to_insert["articles"]),
                                                                                            date_str,
                                                                                            symbol))
                    coll.insert_one(doc_to_insert)
                    total_articles_inserted += len(doc_to_insert["articles"])
            print("************************************************************")
            print("Inserted {0} total articles (that weren't already present) into the "
                  "{1} collection of the news database.".format(total_articles_inserted, symbol))
            print("---------------------------------------")
            print("Sleeping for 30 seconds to avoid IP ban")
            print("************************************************************")
            time.sleep(30)


def get_news_data(symbol):
    mc = MongoClient()
    coll = mc["news"][symbol]
    # d25 = date(2016, 11, 25)
    # start_dt = datetime.combine(d25, datetime.min.time())
    # end_dt = datetime.combine(date.today(), datetime.min.time())

    # cursor = coll.find({"date": {"$lte":end_dt, "$gte":start_dt}}).sort("date", -1)
    end_dt = date.today()
    start_dt = date.today() - timedelta(days=30)
     # now coerce dates to datetimes so we can filter queries by dates
    start_dt = datetime.combine(start_dt, datetime.min.time())
    end_dt = datetime.combine(end_dt, datetime.min.time())
    cursor = coll.find({"date":{"$lte":end_dt, "$gte":start_dt}}).sort("Date", -1)
    articles = []
    for c in cursor:
        if "articles" in c:
            for article in c["articles"]:
                articles.append(article)
    return articles

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Add historical news data to"\
                                         "to the individual DJIA collections of the"\
                                         " news database")

    argparser.add_argument("--insert", action="store_true",
                           help="Insert as much new news data as possible")

    argparser.add_argument("--list", type=str, nargs="?",
                           help="--list <symbol> e.g. --list AAPL")

    args, leftovers = argparser.parse_known_args()

    if args.insert:
        insert_djia_news()
    elif args.list:
        print(args.list)
        get_news_data(args.list)

