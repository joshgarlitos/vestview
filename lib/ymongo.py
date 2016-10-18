import pymongo
import yfinance
import datetime

from pymongo import MongoClient

class YMongo():
    

    def __init__(self, database, collection, user=None, password=None, hostname="localHost", port=27017):
        """
		Initializes connection to the MongoDb Database
        
        Parameters
        ----------
        collection : str
        database : str
        user : str, optional
        password: str, optional
        hostname: str, optional
            default: "localHost"
        port: int, optional
            default:27017
        """
        if user and password:
            db_uri = "mongodb://{user}:{pwd}@{host}:{port}".format(user=username,
                                                                    pwd=password,
                                                                    host=hostname,
                                                                    port=str(port))

        else:
            db_uri = "mongodb://{host}:{port}".format(host=hostname, port=str(port))

        self.db_conn = MongoClient(db_uri)
        self.collection = self.db_conn.get_database(database).get_collection(collection)
        self.yf = yfinance.YFinance()

    def add_stock(self, symbol, start_dt, end_dt):
        """
        Inserts a stock's historical data into the collection, from start_dt to end_dt IF 
        it doesn't exist already.

        Parameters
        ----------
        symbol: str
            Ticker symbol of stock to add into database
        start_dt: str
            "yyyy-mm-dd"
        end_dt: str
            "yyyy-mm-dd"

        """
        exists_in_db = self.collection.find_one({'symbol': symbol})

        if not exists_in_db:
            #gets the stock data from Yahoo Finance using YFinance object interface
            stock_data = self.yf.get_historical([symbol], start_dt, end_dt)
            document_schema = {
                "symbol": symbol,
                "daily_quotes":[
                ]
            }
            for daily_quote in stock_data:
                quote_to_be_inserted = {
                    "date": daily_quote["Date"],
                    "values":{ "open":daily_quote["Open"],
                                "high":daily_quote["High"],
                                "low":daily_quote["Low"],
                                "close":daily_quote["Close"],
                                "volume":daily_quote["Volume"]
                            }
                }
                document_schema["daily_quotes"].append(quote_to_be_inserted)

            self.collection.insert_one(document_schema)

    def add_djia_stocks(self):
        """
        Adds the past 30 days of each DJIA stock to the database.

        NOTE: With current implementation, if the stock already exists in the database, nothing
        will be added. 

        TODO: Fix add_stock to allow updates to certain stocks
        """
        DJIA = ["MMM", "AXP", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DIS",
        "DD", "XOM", "GE", "GS", "HD", "IBM", "INTC", "JNJ", "JPM",
        "MCD", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV", "UTX", "UNH",
        "VZ", "V", "WMT"]

        end_dt = datetime.datetime.today().strftime("%Y-%m-%d")
        start_dt = (datetime.datetime.today() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        for stock in DJIA:
            self.add_stock(stock, start_dt, end_dt)
    def list_stored_stocks(self):
        """
        Returns a list of all stocks stored in database
        """
        stored_stocks = []
        FIELDS = {"symbol":True}
        for stock in self.collection.find(projection=FIELDS):
            stored_stocks.append(stock['symbol'])


        return stored_stocks


    def get_stock(self, symbol):
        FIELDS = {"symbol":True, "daily_quotes":True, "_id":False}
        json_quotes = self.collection.find_one({"symbol":symbol})['daily_quotes']
        return json_quotes

    def __str__(self):
        return str(self.db_conn)

    def __repr__(self):
        return str(self.db_conn)

    def __enter__(self):
        return self.collection

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                print("Database error: can't connect")
                raise exc_type
        finally:
            self.db_conn.close()