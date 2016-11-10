import json
import requests
from datetime import datetime, date
PUBLIC_API_URL = 'http://query.yahooapis.com/v1/public/yql?'
DATATABLES_URL = 'store://datatables.org/alltableswithkeys'
HISTORICAL_URL = 'http://ichart.finance.yahoo.com/table.csv?s='
ALL_DATATABLES_URL = "store://datatables.org/alltableswithkeys"
FINANCE_TABLES = {'quotes': 'yahoo.finance.quote',
                  'options': 'yahoo.finance.options',
                  'quoteslist': 'yahoo.finance.quoteslist',
                  'sectors': 'yahoo.finance.sectors',
                  'industry': 'yahoo.finance.industry',
                  'historical': 'yahoo.finance.historicaldata'}
YQL_BASE_QUERY =  "SELECT * FROM {table} WHERE {key} IN {symbols}"
YQL_HISTORICAL_QUERY =  "SELECT * FROM {table} WHERE {key} in {symbols} and "\
                        "startDate={start_date} and endDate={end_date}"



def get_quote(symbols):
    """
    Queries the public Yahoo Finance API for quotes.

    Parameters
    ----------
    symbols : list-like
        The list of symbols to get quotes for
    Returns
    -------
    List of JSON objects, with each JSON object corresponding to a symbol.
    """

    # have to format symbols list to from ("SYM1", "SYM2", .... ,"SYMN")
    symbols = "(" + ",".join(['\"' + s.upper() + '"' for s in symbols]) + ")"
    yql = YQL_BASE_QUERY.format(table=FINANCE_TABLES["quotes"], key="symbol",
                                symbols=symbols)
    payload = {
        "q": yql,
        "format": "json",
        "env": ALL_DATATABLES_URL
    }
    try:
        resp = requests.get(PUBLIC_API_URL, params=payload)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e)

    return json.loads(resp.text)["query"]["results"]["quote"]

def get_historical(symbols, start_dt, end_dt):
    """
    Queries Yahoo Finance API for daily historical quotes (in the specified range).
    This data includes daily high, lows, and opening prices.

    Parameters
    ----------
    symbols : list-like
        List of symbols to get daily quotes for
    start_dt : string ("yyyy-mm-dd")
        The start of the range, inclusive
    end_dt : string ("yyyy-mm-dd")
        The end of the range, inclusive
    """
    if isinstance(start_dt, date) or isinstance(start_dt, datetime):
        start_dt = start_dt.strftime("%Y-%m-%d")
    if isinstance(end_dt, date) or isinstance(end_dt, datetime):
        end_dt = end_dt.strftime("%Y-%m-%d")

    symbols = "(" + ",".join(['\"' + s.upper() + '"' for s in symbols]) + ")"
    yql = YQL_HISTORICAL_QUERY.format(table=FINANCE_TABLES["historical"], key="symbol",
                                symbols=symbols, start_date='"' + start_dt + '"',
                                end_date= '"' + end_dt + '"')
    if start_dt == end_dt:
        print("start_dt and end_dt are equal, so returning")
        return

    print("Getting historical data from Yahoo Finance API from ", start_dt, " to ", end_dt)

    payload = {
        "q": yql,
        "format": "json",
        "env": ALL_DATATABLES_URL
    }
    try:
        resp = requests.get(PUBLIC_API_URL, params=payload)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e)

    try:
        ret = json.loads(resp.text)["query"]["results"]["quote"]
    except TypeError:
        print("YahooFinance query returned nothing, this is probably due to"
                         " an invalid date range (e.g. too big, or invalid)")
        return

    return ret


if __name__ == "__main__":
    print(get_quote(["GOOG", "MSFT"]))
    print(get_historical(["GOOG"], "2015-10-01", "2015-10-10"))
