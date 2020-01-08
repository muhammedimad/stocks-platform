from django.test import TestCase
from django.http import HttpRequest
import unittest
import requests

#Unit test to check if the response.status_code is 200 for the API "most active stocks"
#Run command: python3 manage.py test myapp.tests
class APITest(unittest.TestCase):

    def setUp(self):
        TestCase.__init__(self)
        self.base_url = 'https://sandbox.iexapis.com/stable/stock/market/list/mostactive?token=Tpk_c818732500c24764801eb121fa658bb6'

    def testApi(self):
        response = requests.get(self.base_url)
        # print(response.status_code)
        self.assertEqual(response.status_code, 200)
 
if __name__ == "__main__":
    unittest.main()

