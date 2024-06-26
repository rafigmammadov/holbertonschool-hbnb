#!/usr/bin/python3
from flask import Flask
from flask_restx import Api
from API.api_users import ns_users
from API.api_country_city import ns_country, ns_city
from API.api_places import ns_places
from API.api_reviews import ns_reviews
from API.api_amenity import ns_amenities


app = Flask(__name__)
api = Api(app, version='1.0', title='HBnB API', description='HBnB application')
api.add_namespace(ns_users)
api.add_namespace(ns_city)
api.add_namespace(ns_country)
api.add_namespace(ns_places)
api.add_namespace(ns_reviews)
api.add_namespace(ns_amenities)

if __name__ == '__main__':
    app.run(debug=True)