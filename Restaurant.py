class Restaurant:
    yelp_id = None
    name = None
    mobile_url = None
    categories = None
    rating = None
    neighborhoods = None

    def __init__(self, id, name, mobile_url, categories, rating, neighborhoods):
        self.yelp_id = id
        self.name = name
        self.mobile_url = mobile_url
        self.categories = categories
        self.rating = rating
        self.neighborhoods = neighborhoods
