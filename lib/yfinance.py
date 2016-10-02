import json 
import requests

PUBLIC_API_URL = 'http://query.yahooapis.com/v1/public/yql?'
DATATABLES_URL = 'store://datatables.org/alltableswithkeys'
HISTORICAL_URL = 'http://ichart.finance.yahoo.com/table.csv?s='
ALL_DATATABLES_URL = "store://datatables.org/alltableswithkeys"
FINANCE_TABLES = {'quotes': 'yahoo.finance.quotes',
                  'options': 'yahoo.finance.options',
                  'quoteslist': 'yahoo.finance.quoteslist',
                  'sectors': 'yahoo.finance.sectors',
                  'industry': 'yahoo.finance.industry'}
YQL_BASE_QUERY =  "SELECT * FROM {table} WHERE {key} IN {symbols}"

class YFinance():
    """
    Provides an interface to the Yahoo Finance API.
    """
    def __init__(self):
        pass

    def get_quote(self, symbols):
        """
        Queries the public Yahoo Finance API and returns a list of JSON objects
        corresponding to the symbols passed in.

        Parameters
        ----------

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


if __name__ == "__main__":
    yf = YFinance()
    print(yf.get_quote(["GOOG"]))
