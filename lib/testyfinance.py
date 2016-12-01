from yfinance import *
import unittest



class TestYFinance(unittest.TestCase):
    
    def test_json(self):
        resp = get_quote(["GOOG"])
        
        self.assertTrue(isinstance(resp, dict))
       
    def test_keys(self):
        resp = get_quote(["GOOG"])
        resp_keys = list(resp.keys())
        
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

        for key in expected_keys:
            self.assertTrue(key in resp_keys)

if __name__ == '__main__':
	unittest.main()
	