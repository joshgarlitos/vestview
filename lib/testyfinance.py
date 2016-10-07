from yfinance import *
import unittest

expected_keys = ['Name',
'Volume',
'YearHigh',
'Change',
'DaysHigh',
'MarketCapitalization',
'AverageDailyVolume',
'YearLow',
'Symbol',
'DaysLow',
'DaysRange',
'LastTradePriceOnly',
'StockExchange',
'symbol']

class TestYFinance(unittest.TestCase):
    
    def test_json(self):
        resp = YFinance.get_quote(self, ["GOOG"])
        self.assertTrue(isinstance(resp, dict))
       
    def test_keys(self):
        resp = YFinance.get_quote(self, ["GOOG"])
        resp_keys = list(resp.keys())

        for key in expected_keys:
            self.assertTrue(key in resp_keys)

if __name__ == 'main':
	unittest.main();
	





