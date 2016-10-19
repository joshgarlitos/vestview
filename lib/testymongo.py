from pymongo import MongoClient
from ymongo import *
import unittest


class TestYMongo(unittest.TestCase):

    def test_stock_in_db(self):
        """
        Ensures that a stock exists in the MongoDB after calling ym.add_stock
        This check is done  using the pymongo API, instantiating a mongoclient, and
        then directly calling `find_one` on the desired colleciton
        """
        #intialize both YMongo class, and pymongo MongoClient to interact with DB
        
        ym = YMongo("vestview", "stocks")
        #defualt port and host
        mc = MongoClient("localHost", 27017)
        db = mc.vestview #database
        stocks = db.stocks #collection

        end_dt = datetime.datetime.today().strftime("%Y-%m-%d")
        start_dt = (datetime.datetime.today() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")

        ym.add_stock("KO", start_dt, end_dt)

        exists_in_db = stocks.find_one({'symbol':'KO'})

        self.assertTrue(exists_in_db)


    def test_get_stock(self):
        """
        Under the assumption that add_stock works, this test will make sure that 
        `get_stock` retrieves the data correctly
        """

        ym = YMongo("vestview", "stocks")
        #defualt port and host
        mc = MongoClient("localHost", 27017)
        db = mc.vestview #database
        stocks = db.stocks #collection

        end_dt = datetime.datetime.today().strftime("%Y-%m-%d")
        start_dt = (datetime.datetime.today() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        ym.add_stock("AAPL", start_dt, end_dt)

        result = ym.get_stock("AAPL")
        expected = stocks.find_one({"symbol":"AAPL"})['daily_quotes']

        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()

