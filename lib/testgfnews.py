from gfnews import *
import unittest

class TestGFNews(unittest.TestCase):
	
	def test_get_news(self):	
		news = get_news(["AAPL"])
		for article in news:
			self.assertTrue(isinstance(article, dict))

	def test_get_data(self):
		article = get_news_data('IBM')
		self.assertTrue(isinstance(article, list))



if __name__ == '__main__':
	unittest.main()
	
