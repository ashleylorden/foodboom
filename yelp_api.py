from restaurant import Restaurant
import ConfigParser
from search import yelp_request
import json
import os
from math import asin, cos, pi, sin


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
                'category_filter': 'restaurants',
                'limit': 5
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

    def search_similar_restaurants(self, restaurant, lat_lon=None, bearing=None):
        #  rest not closed, matching cats, limit 15
        if not lat_lon:
            lat_lon = '37.7872247,-122.39926'
        lat, lon = lat_lon.split(',')
        if not bearing:
            results = yelp_request(
                'search',
                {
                    'term': 'restaurant',
                    'limit': 15,
                    'category_filter': restaurant.get_categories().lower(),
                    'sort': 1,
                    'll': lat_lon,
                },
                self.consumer_key,
                self.consumer_secret,
                self.token,
                self.token_secret
            )
        else:
            lat1, lon1, lat2, lon2 = get_yelp_coordinates(lat, lon, bearing, 2)
            # lat2, lon2 = pointRadialDistance(lat, lon, bearing, 5.8)
            print "L1: %s" % lat_lon
            print "L2: %s,%s" % (lat2, lon2)
            results = yelp_request(
                'search',
                {
                    'term': 'restaurant',
                    'limit': 15,
                    'category_filter': restaurant.get_categories().lower(),
                    'sort': 1,
                    'bounds': "%s,%s|%s,%s" % (lat1, lon1, lat2 ,lon2)
                },
                self.consumer_key,
                self.consumer_secret,
                self.token,
                self.token_secret
            )

        # Put them on a list except the closed ones
        restaurants = []
        if not results.get('businesses'):
            return []
        for result in results.get('businesses', None):
            if not result.get('is_closed') and \
                    result.get('id') != restaurant.yelp_id:
                r = Restaurant()
                r.load_data(result)
                restaurants.append(r)

        # Sort by rating
        restaurants = sorted(restaurants, key=lambda r: r.rating, reverse=True)

        # Keep top 3
        restaurants = restaurants[1:4]

        return restaurants

def get_yelp_coordinates(lat, lon, bearing, distance):
    # Get coordinates of half the distance going to bearing = center
    distance = float(distance) / 2
    center_lat, center_lon = pointRadialDistance(lat, lon, bearing, distance)
    lat1, lon1 = pointRadialDistance(center_lat, center_lon, 135, distance)
    lat2, lon2 = pointRadialDistance(center_lat, center_lon, 315, distance)
    return lat1, lon1, lat2, lon2


rEarth = 6371.01 # Earth's average radius in km
epsilon = 0.000001 # threshold for floating-point equality


def deg2rad(angle):
    return float(angle) * float(pi) / 180


def rad2deg(angle):
    return float(angle) * 180 / float(pi)


def pointRadialDistance(lat1, lon1, bearing, distance):
    """
    Return final coordinates (lat2,lon2) [in degrees] given initial coordinates
    (lat1,lon1) [in degrees] and a bearing [in degrees] and distance [in km]
    """
    rlat1 = deg2rad(lat1)
    rlon1 = deg2rad(lon1)
    rbearing = deg2rad(bearing)
    rdistance = distance / rEarth # normalize linear distance to radian angle

    rlat = asin( sin(rlat1) * cos(rdistance) + cos(rlat1) * sin(rdistance) * cos(rbearing) )

    if cos(rlat) == 0 or abs(cos(rlat)) < epsilon: # Endpoint a pole
        rlon=rlon1
    else:
        rlon = ( (rlon1 - asin( sin(rbearing)* sin(rdistance) / cos(rlat) ) + pi ) % (2*pi) ) - pi

    lat = rad2deg(rlat)
    lon = rad2deg(rlon)
    return (lat, lon)


#y = YelpAPI()
#
#r = y.get_restaurant("yum-yum-hunan-san-francisco-2")
#print r
#
#results = y.search_similar_restaurants(r)
#for r in results:
#    print r
