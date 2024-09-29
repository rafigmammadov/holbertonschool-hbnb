from flask import request, jsonify
from flask_restx import Namespace, Resource, fields, Api
from app import db
from models import Amenity
from datetime import datetime

# Namespace
ns_amenities = Namespace('amenities', description='Amenity operations')

# Model for serialization/deserialization
amenity_model = ns_amenities.model('Amenity', {
    'id': fields.String(readOnly=True, description='The amenity identifier'),
    'name': fields.String(required=True, description='The amenity name'),
    'description': fields.String(required=True, description='The amenity description'),
    'created_at': fields.String(description='The amenity creation timestamp'),
    'updated_at': fields.String(description='The amenity update timestamp')
})

# Resource routes
@ns_amenities.route('/')
class AmenityList(Resource):
    @ns_amenities.doc('list_amenities')
    @ns_amenities.marshal_list_with(amenity_model)
    def get(self):
        """List all amenities"""
        amenities = Amenity.query.all()
        return amenities

    @ns_amenities.doc('create_amenity')
    @ns_amenities.expect(amenity_model)
    @ns_amenities.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        data = request.json
        amenity = Amenity(name=data['name'], description=data['description'])
        db.session.add(amenity)
        db.session.commit()
        return amenity, 201

@ns_amenities.route('/<string:id>')
@ns_amenities.response(404, 'Amenity not found')
@ns_amenities.param('id', 'The amenity identifier')
class AmenityResource(Resource):
    @ns_amenities.doc('get_amenity')
    @ns_amenities.marshal_with(amenity_model)
    def get(self, id):
        """Fetch a single amenity"""
        amenity = Amenity.query.filter_by(id=id).first()
        if not amenity:
            ns_amenities.abort(404, message="Amenity not found")
        return amenity

    @ns_amenities.doc('update_amenity')
    @ns_amenities.expect(amenity_model)
    @ns_amenities.marshal_with(amenity_model)
    def put(self, id):
        """Update an existing amenity"""
        data = request.json
        amenity = Amenity.query.filter_by(id=id).first()
        if not amenity:
            ns_amenities.abort(404, message="Amenity not found")
        amenity.name = data['name']
        amenity.description = data['description']
        amenity.updated_at = datetime.utcnow()
        db.session.commit()
        return amenity

    @ns_amenities.doc('delete_amenity')
    @ns_amenities.response(204, 'Amenity deleted')
    def delete(self, id):
        """Delete an amenity"""
        amenity = Amenity.query.filter_by(id=id).first()
        if not amenity:
            ns_amenities.abort(404, message="Amenity not found")
        db.session.delete(amenity)
        db.session.commit()
        return '', 204

# Add namespace to API
api = Api()
api.add_namespace(ns_amenities)

