from restaurant import Restaurant
import ConfigParser
from search import yelp_request
import json
import os


class YelpAPI:

    consumer_key = ''
    consumer_secret = ''
    token = ''
    token_secret = ''

    def __init__(self):
#        config = ConfigParser.ConfigParser()
#        config.read("config.ini")
#        self.consumer_key = config.get("yelp", "consumer_key")
#        self.consumer_secret = config.get("yelp", "consumer_secret")
#        self.token = config.get("yelp", "token")
#        self.token_secret = config.get("yelp", "token_secret")
        self.consumer_key = os.environ['consumer_key']
        self.consumer_secret = os.environ['consumer_secret']
        self.token = os.environ['token']
        self.token_secret = os.environ['token_secret']

    def search_restaurant(self, string):
        results = yelp_request(
            'search',
            {
                'term': string,
                'location': 'San Francisco',
                'limit': 3
            },
            self.consumer_key,
            self.consumer_secret,
            self.token,
            self.token_secret
        )

        restaurants = []
        for result in results.get('businesses', None):
            r = Restaurant()
            r.load_data(result)
            restaurants.append(r)
        return restaurants

    def get_restaurant(self, restaurant_id):
        result = yelp_request(
            'business',
            {'id': restaurant_id},
            self.consumer_key,
            self.consumer_secret,
            self.token,
            self.token_secret
        )
        restaurant = Restaurant()
        restaurant.load_data(result)
        return restaurant

    def search_similar_restaurants(self, restaurant):
        #  rest not closed, matching cats, limit 15
        results = yelp_request(
            'search',
            {
                'term': 'restaurant',
                'location': '%s, %s' % (restaurant.address, restaurant.city),
                'limit': 15,
                'category_filter': restaurant.get_categories().lower(),
                'sort': 1,
                'cll': '37.78646,-122.4400427'
            },
            self.consumer_key,
            self.consumer_secret,
            self.token,
            self.token_secret
        )

        # Put them on a list except the closed ones
        restaurants = []
        for result in results.get('businesses', None):
            if not result.get('is_closed'):
                r = Restaurant()
                r.load_data(result)
                restaurants.append(r)

        # Sort by rating
        restaurants = sorted(restaurants, key=lambda r: r.rating, reverse=True)

        # Keep top 3
        restaurants = restaurants[1:4]

        return restaurants


#y = YelpAPI()
#
#r = y.get_restaurant("yum-yum-hunan-san-francisco-2")
#print r
#
#results = y.search_similar_restaurants(r)
#for r in results:
#    print r
