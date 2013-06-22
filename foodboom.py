from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, json

import yelp_api, restaurant

app = Flask(__name__)
app.config.from_object(__name__)

yelp = YelpAPI()

def to_json(restaurant_list):
    list_to_return = []
    for restaurant in restaurant_list:
        list_to_return.append(restaurant.__dict__)
    return jsonify(list_to_return)

@app.route('/search/<search_term>')
def search(search_term=None):
    restaurants = []
    if search_term:
        restaurants = yelp.search_restaurant(search_term)
    return to_json(restaurants)

@app.route('/similar/<yelp_id>')
def similar(yelp_id=None):
    restaurants = []
    if yelp_id:
        selected_restaurant = yelp.get_restaurant(yelp_id)
        restaurants = yelp.search_similar_restaurants(selected_restaurant)
    return to_json(restaurants)

if __name__ == '__main__':
    app.run()
