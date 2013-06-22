#from restaurant import Restaurant
import ConfigParser


class YelpAPI:

    consumer_key = ''
    consumer_secret = ''
    token = ''
    token_secret = ''

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read("config.ini")
        self.consumer_key = config.get("yelp", "consumer_key")
        self.consumer_secret = config.get("yelp", "consumer_secret")
        self.token = config.get("yelp", "token")
        self.token_secret = config.get("yelp", "token_secret")

    def search_restaurant(self, string):
        pass

    def get_restaurant(self, restaurant_id):
        pass

    def search_similar_restaurants(self, restaurant):
        pass
