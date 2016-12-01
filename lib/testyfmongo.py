from yfmongo import*
import unittest

class TestYFMongo(unittest.TestCase):

	def test_get_stock_data(self):
		yfm = YFMongo("vestview", "stocks")
		data = yfm.get_stock_data('AAPL')
		for ins in data:
			self.assertTrue(isinstance(ins, dict))
		






if __name__ == '__main__':
	unittest.main()
	