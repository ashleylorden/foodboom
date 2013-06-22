class Restaurant:
    yelp_id = None
    name = None
    mobile_url = None
    categories = None
    rating = None
    neighborhoods = None

    def __init__(self, id=None, name=None, mobile_url=None, categories=None,
                 rating=None, neighborhoods=None):
        self.yelp_id = id
        self.name = name
        self.mobile_url = mobile_url
        self.categories = categories
        self.rating = rating
        self.neighborhoods = neighborhoods

    def load_data(self, dictionary):
        if "id" in dictionary:
            self.yelp_id = dictionary["id"]
        if "name" in dictionary:
            self.name = dictionary["name"]
        if "mobile_url" in dictionary:
            self.mobile_url = dictionary["mobile_url"]
        if "categories" in dictionary:
            self.categories = dictionary["categories"]
        if "rating" in dictionary:
            self.rating = dictionary["rating"]
        if "location" in dictionary:
            if "neighborhoods" in dictionary["location"]:
                self.neighborhoods = dictionary["location"]["neighborhoods"]

    def __str__(self):
        return """%s -- %s
        Rating: %s
        %s
        %s
        %s""" % (self.yelp_id, self.name, self.rating, self.categories, 
                 self.neighborhoods, self.mobile_url)
