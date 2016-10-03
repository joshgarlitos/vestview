import json 
import requests

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

class YFinance():
    """
    Provides an interface to the Yahoo Finance API.
    """
    def __init__(self):
        pass

    def get_quote(self, symbols):
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

    def get_historical(self, symbols, start_dt, end_dt):
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
        symbols = "(" + ",".join(['\"' + s.upper() + '"' for s in symbols]) + ")"
        yql = YQL_HISTORICAL_QUERY.format(table=FINANCE_TABLES["historical"], key="symbol",
                                    symbols=symbols, start_date='"' + start_dt + '"',
                                    end_date= '"' + end_dt + '"')

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


if __name__ == "__main__":
    yf = YFinance()
    print(yf.get_quote(["GOOG", "MSFT"]))
    print(yf.get_historical(["GOOG"], "2015-10-01", "2015-10-10"))