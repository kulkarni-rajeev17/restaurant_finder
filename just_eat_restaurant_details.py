'''

This programme extracts details of all resturants in a given PostalCode.
The user can filter the results based on his choice of Cuisine
URL Endpoint: https://uk.api.just-eat.io/restaurants/bypostcode/{PostCode}
I have filtered the results based on cuisine by my logic and understanding
as the URL endpoint was giving the same results as with a postcode.
@Author - Rajeev.Kulkarni
Date-11/7/2020
'''


import requests
import pandas as pd
from datetime import datetime
import os


class JustEatApi:

    def __init__(self):
        self.api_endpoint_url = 'https://uk.api.just-eat.io/restaurants/bypostcode/'

    # Makes the request to the public api and get the resturant_data from this
    def make_request(self, url):

        try:
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                    '(KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
            response = requests.get(url, headers=header)

        except Exception as e:
            print("Exception occured while making request", e.message)
            exit(1)

        if response.status_code < 200 or response.status_code >= 400:
            raise Exception("Invalid URL")

        return response.json()


    # Handles the api request and parsing of data from the api
    def handle_request(self, post_code, cuisine=None):
        if cuisine:
            url = self.api_endpoint_url + post_code + '?cuisine=' + cuisine
        else:
            url = self.api_endpoint_url + post_code

        restaurant_data_json = self.make_request(url)
        restaurant_data = self.parse_data(restaurant_data_json, cuisine)
        self.write_to_file(restaurant_data)
        if not restaurant_data.empty:
            print(restaurant_data.to_string(index=False))



    # Parses the data recievced from the public api and sorts the data based on Post_Code or by PostCode and cuisine
    #It then orders the result by Ratings.
    def parse_data(self, values, cuisine=None):

        count = 0
        data = []

        #Goes through the restaurant collenction from json and extracts key information
        for restaurant in values["Restaurants"]:
            if cuisine:
                if any(cuisines['SeoName'] == cuisine.lower() for cuisines in restaurant["Cuisines"]):
                    data.append([restaurant["Name"], restaurant["City"], restaurant["RatingStars"],restaurant["DeliveryOpeningTimeLocal"]])
                    count+=1
            else:
                data.append([restaurant["Name"], restaurant["City"], restaurant["RatingStars"],restaurant["DeliveryOpeningTimeLocal"]])
                count += 1
        df = pd.DataFrame(data, columns=['Name', 'City', 'RatingStars','OpeningTime'])


        #If there are resturants returned in a particular area it sorts them
        if count:
            df = df.sort_values('RatingStars', ascending=False)
        else:
            print("No resturants found in this area, please check your postcode  or cuisine again")
        return df


    def write_to_file(self, restaurant_data):
        now = datetime.now()
        today = now.strftime("%Y%m%d_%H%M%S")
        filename = "justeat_" + today + ".csv"
        restaurant_data.to_csv(filename, index=False)

    def main(self):

        while 1:
            postcode = input("Enter your PostCode (press q to quit): ")

            if postcode.lower() == 'q':
                print("Thank you!")
                exit(0)

            elif postcode == '' or len(postcode) < 4 or len(postcode) > 8:
                print("Please enter a valid PostCode")

            else:
                postcode = postcode.upper()
                postcode=postcode.lstrip()
                postcode=postcode.rstrip()
                option = input("Type Yes to search resturant by cuisines or NO or continue your search: ")
                option = option.lower()
                if option == 'yes' or option == 'y':
                    cuisine = input("Enter your cuisine: ")
                    cuisine.lower()
                    self.handle_request(postcode, cuisine)
                elif option == 'no' or option == 'n':
                    self.handle_request(postcode)


if __name__ == "__main__":
    justEatApi = JustEatApi()
    justEatApi.main()

