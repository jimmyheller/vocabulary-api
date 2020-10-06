from django.test import TestCase
import requests
from .translator import translator


# Create your tests here.

class RandomAPiTestCases(TestCase):

	def test_random_word(self):
		request = requests.get("http://127.0.0.1:8000/api/v1/random-word/")
		self.assertEqual(request.status_code, 200)

	def test_vast_random_word(self):
		for i in range(50):
			request = requests.get("http://127.0.0.1:8000/api/v1/random-word/")
			self.assertEqual(request.status_code, 200)


class WordTranslator(TestCase):

	def test_hello(self):
		self.assertEqual(translator("hello", source='en', destination='fa'), 'سلام')

	def test_admit_wrong(self):
		self.assertEqual(translator("admit", source='en', destination='fa'), 'اقرار')
