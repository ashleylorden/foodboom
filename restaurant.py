class Restaurant:
    yelp_id = None
    name = None
    mobile_url = None
    categories = None
    rating = None
    address = None
    city = None

    def __init__(self, yelp_id=None, name=None, mobile_url=None, categories=None,
                 rating=None, address=None, city=None):
        self.yelp_id = yelp_id
        self.name = name
        self.mobile_url = mobile_url
        self.categories = categories
        self.rating = rating
        self.address = address
        self.city = city

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
            if "address" in dictionary["location"]:
                self.address = dictionary["location"]["address"]
            if "city" in dictionary["location"]:
                self.city = dictionary["location"]["city"]

    def get_categories(self):
        l = []
        for category in self.categories:
            l.append(category[0])
        return ','.join(l)

    def __str__(self):
        return """%s -- %s
        Rating: %s
        %s
        %s, %s
        %s""" % (self.yelp_id, self.name, self.rating, self.categories, 
                 self.address, self.city, self.mobile_url)
