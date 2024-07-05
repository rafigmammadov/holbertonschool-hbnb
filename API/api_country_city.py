from flask import request
from flask_restx import Api, Resource, Namespace, fields
from app import db
from models import Country, City
from persistence.data_manager import DataManager
import json

# Initialize Flask application and Flask-RestX API
app = Flask(__name__)
api = Api(app, version='1.0', title='Country and City API', description='A simple Country and City API')

# Initialize DataManager with JSON file
data_manager = DataManager("database.json")

# Load ISO 3166-1 data from JSON file
def load_iso_3166_1_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

# Namespace definitions
ns_country = Namespace('countries', description='Country related operations')
ns_city = Namespace('cities', description='City related operations')

# Load ISO 3166-1 data and create Country objects
iso_3166_1_data = load_iso_3166_1_data('countries.json')
countries = {code: Country(code, name) for code, name in iso_3166_1_data.items()}

# Model definitions for serialization/deserialization
country_response_model = ns_country.model('Country', {
    'name': fields.String(required=True, description='Name of the country'),
    'country_code': fields.String(required=True, description='Code of the country')
})

city_request_model = ns_city.model('CityRequest', {
    'country': fields.String(required=True, description='Code of the country'),
    'name': fields.String(required=True, description='Name of the city')
})

city_response_model = ns_city.model('CityResponse', {
    'id': fields.String(description='The city unique identifier'),
    'name': fields.String(required=True, description='Name of the city'),
    'country': fields.String(required=True, description='Country code of the city'),
    'created_at': fields.String(description='The city creation timestamp'),
    'updated_at': fields.String(description='The city update timestamp')
})

# Resource routes for countries
@ns_country.route('/')
class CountryList(Resource):
    @ns_country.doc('list_countries')
    @ns_country.marshal_list_with(country_response_model)
    def get(self):
        """List all countries"""
        return [country.to_dict() for country in countries.values()]

@ns_country.route('/<string:country_code>')
class CountryGet(Resource):
    @ns_country.doc('get_country_by_code')
    @ns_country.marshal_with(country_response_model)
    def get(self, country_code):
        """Fetch a single country by code"""
        if country_code in countries:
            return countries[country_code].to_dict(), 200
        else:
            api.abort(404, f"Country with code '{country_code}' not found.")

@ns_country.route('/<string:country_code>/cities')
class CountryGetCity(Resource):
    @ns_country.doc('get_cities_of_country')
    @ns_country.marshal_list_with(city_response_model)
    def get(self, country_code):
        """List all cities of a specific country"""
        if country_code in countries:
            return [city.to_dict() for city in countries[country_code].cities], 200
        else:
            api.abort(404, f"Country with code '{country_code}' not found.")

# Resource routes for cities
@ns_city.route('/')
class CityGetPost(Resource):
    @ns_city.doc('post_city')
    @ns_city.expect(city_request_model)
    @ns_city.marshal_with(city_response_model, code=201)
    def post(self):
        """Create a new city"""
        data = request.json
        try:
            country_code = data['country']
            name = data['name']

            if not (country_code and name):
                api.abort(400, "Country and name are required.")

            if country_code not in countries:
                api.abort(404, f"Country with code '{country_code}' not found.")

            existing_city = data_manager.get_by_field('name', name, 'City')
            if existing_city:
                api.abort(409, "City already exists.")

            city = City(country=country_code, name=name)
            countries[country_code].add_city(city)
            data_manager.save(city)

            return city.to_dict(), 201

        except KeyError:
            api.abort(400, "Invalid input format.")

    @ns_city.doc('list_cities')
    @ns_city.marshal_list_with(city_response_model)
    def get(self):
        """List all cities"""
        cities = []
        data = data_manager._read_data()
        if 'City' in data:
            cities = list(data['City'].values())
        return cities, 200

@ns_city.route('/<string:city_id>')
class CityOperationsID(Resource):
    @ns_city.doc('get_city_by_id')
    @ns_city.marshal_with(city_response_model)
    def get(self, city_id):
        """Fetch a city by ID"""
        city = data_manager.get(city_id, 'City')
        if city:
            return city, 200
        else:
            api.abort(404, "City not found.")

    @ns_city.doc('update_city_by_id')
    @ns_city.expect(city_request_model)
    @ns_city.marshal_with(city_response_model)
    def put(self, city_id):
        """Update a city by ID"""
        data = request.json
        try:
            city = data_manager.get(city_id, 'City')
            if not city:
                api.abort(404, "City not found.")

            updated_city = City(
                country=data.get('country', city['country']),
                name=data.get('name', city['name'])
            )
            updated_city.id = city_id
            data_manager.update(updated_city)
            return updated_city.to_dict(), 200

        except KeyError:
            api.abort(400, "Invalid input format.")

    @ns_city.doc('delete_city_by_id')
    @ns_city.response(204, 'City deleted')
    def delete(self, city_id):
        """Delete a city by ID"""
        city = data_manager.get(city_id, 'City')
        if not city:
            api.abort(404, "City not found.")

        data_manager.delete(city_id, 'City')
        return '', 204

# Add namespaces to API
api.add_namespace(ns_country)
api.add_namespace(ns_city)

if __name__ == "__main__":
    app.run(debug=True)

