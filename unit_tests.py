
'''
This programme extracts details of all resturants in a given PostalCode.
The user can filter the results based on his choice of Cuisine
URL Endpoint: https://uk.api.just-eat.io/restaurants/bypostcode/{PostCode}
I have filtered the results based on cuisine by my logic and understanding as the URL endpoint was giving the same results/
as with a postcode.
@Author - Rajeev.Kulkarni
Date-11/7/2020
'''

import unittest
from just_eat_restaurant_details import JustEatApi


class JustEatApiTest(unittest.TestCase):

    def setUp(self):
        self.just_eat_api = JustEatApi()

    def test_request_call_positive(self):
        valid_url = "https://uk.api.just-eat.io/restaurants/bypostcode/CR26XH"
        self.assertIsNotNone(self.just_eat_api.make_request(valid_url), "Request is empty")

    def test_request_parse_data(self):
        valid_url = "https://uk.api.just-eat.io/restaurants/bypostcode/CR26XH"
        response_json=self.just_eat_api.make_request(valid_url)
        count=response_json["MetaData"]["ResultCount"]
        size_of_dtaframe=len(self.just_eat_api.parse_data(response_json))
        self.assertEqual(count, size_of_dtaframe)
