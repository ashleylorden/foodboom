from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, json, jsonify, make_response

from yelp_api import YelpAPI

app = Flask(__name__)
app.config.from_object(__name__)

yelp = YelpAPI()


def to_json(restaurant_list):
    list_to_return = []
    for restaurant in restaurant_list:
        list_to_return.append(restaurant.__dict__)
    return json.dumps(list_to_return)


@app.route('/')
def home():
    return "Food BOOM!"


@app.route('/search/<search_term>')
def search(search_term=None):
    restaurants = []
    if search_term:
        restaurants = yelp.search_restaurant(search_term)
    res = make_response(to_json(restaurants))
    res.mimetype = 'application/json'
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


@app.route('/similar/<yelp_id>')
def similar(yelp_id=None):
    restaurants = []
    if yelp_id:
        selected_restaurant = yelp.get_restaurant(yelp_id)
        restaurants = yelp.search_similar_restaurants(selected_restaurant)
    res = make_response(to_json(restaurants))
    res.mimetype = 'application/json'
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


@app.route('/similar/<yelp_id>/<lat_lon>')
def similar(yelp_id=None, lat_lon=None):
    restaurants = []
    if yelp_id:
        selected_restaurant = yelp.get_restaurant(yelp_id)
        restaurants = yelp.search_similar_restaurants(
            selected_restaurant, lat_lon)
    res = make_response(to_json(restaurants))
    res.mimetype = 'application/json'
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


if __name__ == '__main__':
    app.run()
