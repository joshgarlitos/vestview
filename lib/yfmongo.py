import pymongo
import datetime
import argparse
import pandas as pd
from yfinance import get_historical, get_quote
from datetime import datetime, date, timedelta
from pymongo import MongoClient


DJIA_STOCKS = [
    "MMM", "AXP", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DIS",
    "DD", "XOM", "GE", "GS", "HD", "IBM", "INTC", "JNJ", "JPM",
    "MCD", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV", "UTX", "UNH",
    "VZ", "V", "WMT"
]

class YFMongo():

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


    def insert_djia_data(self, start_dt, end_dt):
        """
        Inserts daily stock data for all DJIA stocks into the database, with the
        schema:
        {
            "Date": <python datetime object corresponding to day>
            "<AAPL>": {
                    "Adj_Close":float
                    "Close":    float
                    "High":     float
                    "Low":      float
                    "Open":     float
                    "Symbol":   float
                    "Volume":   float
            }
            ....
            ....
            "WMT:"{.....}
        }

        The function will ensure that the timeseries data in the database is continuous,
        and will not overwrite existing data. If the passed in interval
        overlaps with the current database data, it will calculate the correct
        start and end times, and only insert that historical data.

        NOTE: If the passed in interval totally encompasses the current database
        data, it will recurse and split it up into a left and right half.

        For exmaple, let's say the current database holds DJIA data from
        2/1/2016 - 8/1/2016. If we called this function to insert data from
        1/1/2016 - 9/1/2016, it will insert data from 1/1/2016 - 1/31/2016
        and 8/2/2016 - 9/1/2016

        TODO: Implement chunking, when the date range is too big, YF API can't
        rejects the requests. So find threshold and break requests into chunks
        less than that threshold.
        """
        if not isinstance(start_dt, date):
            raise TypeError("start_dt must be a date object")
        if not isinstance(end_dt, date):
            raise TypeError("end_dt must be a date object")
        if start_dt > end_dt:
            raise ValueError("start_dt must occur before end_dt")
        # first grab the earliest and latest entries from the database
        earliest_entry_dt = self.get_earliest_entry_dt()
        latest_entry_dt = self.get_latest_entry_dt()
        today = date.today()
        if end_dt >= today:
            end_dt = today - timedelta(days=1)

        if earliest_entry_dt is None or latest_entry_dt is None:
            empty = True
        else:
            empty = False
        # if the data to be interted is wholly contained by the current data, do nothing
        if not empty and start_dt >= earliest_entry_dt and end_dt <= latest_entry_dt:
            print("*Database already contains data in this range, so nothing is being inserted")
            return
        # refer to doc string, the passed in interval is bigger than current db
        elif not empty and start_dt < earliest_entry_dt and end_dt > latest_entry_dt:
            self.insert_djia_data(start_dt, earliest_entry_dt)
            self.insert_djia_data(latest_entry_dt, end_dt)
            return

        # ensuring continuous timeseries data by modifying interval end points
        if not empty and (start_dt >= earliest_entry_dt or start_dt > end_dt):
            start_dt = latest_entry_dt + timedelta(days=1)

        if not empty and (end_dt <= latest_entry_dt or end_dt < start_dt):
            end_dt = earliest_entry_dt - timedelta(days=1)

        djia_data = get_historical(DJIA_STOCKS, start_dt, end_dt)

        if djia_data is None:
            return
        # coerce the resp date strings to native python date objects
        # this is done so we can sort (and thereby group) the data by date
        for d in djia_data:
            d["Date"] = datetime.strptime(d["Date"], "%Y-%m-%d").date()

        # sort by the date, so the data is grouped by dates, and not companies
        djia_data.sort(key=lambda d: d["Date"])

        # create a list of all business dates we grabbed historical data for
        date_range = pd.date_range(start_dt, end_dt, freq="B").tolist()
        # pd.date_range returns a list of Timestamps, so convert all to dates
        date_range = list(map(lambda t: date(t.year, t.month, t.day), date_range))

        # for each date in the range, create a new document, then add all the
        # cooresponding DJIA stock data for that specific date
        curr_ix = 0
        for curr_date in date_range:
            stock_data_for_curr_date = False
            doc_to_insert = {
            # mongodb can natively store datetimes, but not dates -- so coerce
            "Date" : datetime.combine(curr_date, datetime.min.time())
            }
            # data is sorted, so keep adding stocks with the same date to the doc
            while(curr_ix < len(djia_data) and djia_data[curr_ix]["Date"] == curr_date):
                doc_to_insert[djia_data[curr_ix]["Symbol"]] = {
                    "adjClose":  float(djia_data[curr_ix]["Adj_Close"]),
                    "close":      float(djia_data[curr_ix]["Close"]),
                    #"Date":       doc_to_insert["Date"].strftime("%Y-%m-%d"),
                    "high":       float(djia_data[curr_ix]["High"]),
                    "low":        float(djia_data[curr_ix]["Low"]),
                    "open":       float(djia_data[curr_ix]["Open"]),
                    "volume":     float(djia_data[curr_ix]["Volume"])
                }
                stock_data_for_curr_date = True
                curr_ix += 1

            if stock_data_for_curr_date:
                print("Inserting DJIA data for {0}".format(curr_date.strftime("%m-%d-%Y")))
                self.collection.insert_one(doc_to_insert)

    def update_djia_data(self):
        """
        Extends the DJIA daily stock data from the most recent entry until today.
        If the database is empty, then it will insert the past 30 days.

        TODO: If time (EST) is past 5pm, then set today_dt to today, else
              set it to yesterday
        """

        start_dt = self.get_latest_entry_dt()
        # if there is no such entry (empty db) then we just set it to -30 days
        if start_dt is None:
            start_dt = date.today() - timedelta(days=30)

        end_dt = date.today() - timedelta(days=1)

        if start_dt == end_dt:
            print("Database up to date, not inserting anything...")
            return

        self.insert_djia_data(start_dt, end_dt)


    def get_stock_data(self, symbol):
        """
        Current implementation on front end relies on a month of data,
        so we will just grab a month for now...
        """
        end_dt = date.today()
        start_dt = date.today() - timedelta(days=30)
        # now coerce dates to datetimes so we can filter queries by dates
        start_dt = datetime.combine(start_dt, datetime.min.time())
        end_dt = datetime.combine(end_dt, datetime.min.time())

        cursor = self.collection.find({"Date":{"$lte":end_dt, "$gte":start_dt}},
                                      projection={"Date":True, symbol: True}).sort("Date", -1)
        daily_data = []
        for day in cursor:
            ins = {}
            ins["date"] = day["Date"].strftime("%Y-%m-%d")
            ins["values"] = day[symbol]
            daily_data.append(ins)


        return daily_data




    def get_latest_entry_dt(self):
        # returns a cursor object to the most recent entry in the db
        latest_entry = self.collection.find({}).sort("Date", -1).limit(1)

        if latest_entry.count() == 0:
            return None
        else:
            return latest_entry[0]["Date"].date()

    def get_earliest_entry_dt(self):
        # returns a cursor object to the earliest entry in the db
        earliest_entry = self.collection.find({}).sort("Date", 1).limit(1)

        if earliest_entry.count() == 0:
            return None
        else:
            return earliest_entry[0]["Date"].date()

    def _clear(self):
        res = self.collection.delete_many({})
        print("Delted {0} entires from the vestview/stocks collection...".format(str(res.deleted_count)))

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

    """
    def add_stock(self, symbol, start_dt, end_dt):
        '''
        DEPRECATED FOR OUR USES
        Inserts a stock's historical data into the collection, from start_dt to end_dt
        FOR THE FIRST TIME.

        Parameters
        ----------
        symbol: str
            Ticker symbol of stock to add into database
        start_dt: datetime object
        end_dt: datetime object
        '''
        exists_in_db = self.collection.find_one({'symbol': symbol})
        start_dt_str = start_dt.strftime("%Y-%m-%d")
        end_dt_str = end_dt.strftime("%Y-%m-%d")

        if not exists_in_db:
            #gets the stock data from Yahoo Finance using YFinance object interface
            stock_data = get_historical([symbol], start_dt_str, end_dt_str)
            document_schema = {
                "symbol": symbol,
                "daily_quotes":[]
            }
            for daily_quote in stock_data:
                quote_to_be_inserted = {
                    # insert python native datetime object
                    "date": datetime.strptime(daily_quote["Date"], "%Y-%m-%d"),
                    "values":{ "open":daily_quote["Open"],
                                "high":daily_quote["High"],
                                "low":daily_quote["Low"],
                                "close":daily_quote["Close"],
                                "volume":daily_quote["Volume"]
                            }
                }
                document_schema["daily_quotes"].append(quote_to_be_inserted)
            self.collection.insert_one(document_schema)
    """

def parse_date(date_str):
    """
    Utility function that tries to take date arg (from command line) and turn it
    into a datetime
    """
    date_formats = ["%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d",
                    "%m-%d-%Y", "%m/%d/%Y", "%m.%d.%Y",
                    "%d-%m-%y", "%d/%m/%y", "%d.%m.%y"
                    ]
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            pass
    raise ValueError("couldn't parse dates, please use -h for accepted formats")

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Add historical DJIA stock"\
                                    "data to mongodb from start arg to end arg")
    argparser.add_argument("--update", action="store_true",
                            help="Update daily DJIA date until today")

    argparser.add_argument("--clear", action="store_true",
                           help="Clear the database")

    argparser.add_argument("-s", "--start", type=str,  nargs="?",
                            help="Start date with format"\
                            " YYYY{-/.}MM{-/.}DD or MM{-/.}DD{-/.}YYYY")
    argparser.add_argument("-e", "--end", type=str, nargs="?",
                            help="End date with format"\
                            " YYYY{-/.}MM{-/.}DD or MM{-/.}DD{-/.}YYYY")
    args, leftovers = argparser.parse_known_args()

    yfm = YFMongo("vestview", "stocks")
    if args.update:
        yfm.update_djia_data()
    elif args.clear:
        yfm._clear()
    elif args.start and  args.end:
        start_dt = parse_date(args.start)
        end_dt = parse_date(args.end)
        yfm.insert_djia_data(start_dt, end_dt)
    else:
        print("please supply either BOTH a start and end, or simply --update")



