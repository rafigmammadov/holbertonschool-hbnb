#!/usr/bin/python3
from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from API.api_users import ns_users
from API.api_country_city import ns_country, ns_city
from API.api_places import ns_places
from API.api_reviews import ns_reviews
from API.api_amenity import ns_amenities

# Initialize Flask application
app = Flask(__name__)

# Configure SQLAlchemy for database management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize Flask-RestX API
api = Api(app, version='1.0', title='HBnB API', description='HBnB application')

# Initialize Flask-JWT-Extended for JWT authentication
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this in your actual implementation
jwt = JWTManager(app)

# Add namespaces for different API resources
api.add_namespace(ns_users)
api.add_namespace(ns_city)
api.add_namespace(ns_country)
api.add_namespace(ns_places)
api.add_namespace(ns_reviews)
api.add_namespace(ns_amenities)

if __name__ == '__main__':
    app.run(debug=True)

