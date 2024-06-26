from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields, Namespace
from Model.users import Users
from Persistence.data_manager import DataManager

app = Flask(__name__)
api = Api(app, version='1.0', title='User API', description='A simple User API')

ns_users = Namespace('users', description='User operations')

data_manager = DataManager("database.json")

user_request_model = ns_users.model('UserRequest', {
    'email': fields.String(required=True, description='The user email'),
    'first_name': fields.String(required=True, description='The user first name'),
    'last_name': fields.String(required=True, description='The user last name'),
    'password': fields.String(required=True, description='The user password')
})

user_response_model = ns_users.model('UserResponse', {
    'id': fields.String(description='The user unique identifier'),
    'email': fields.String(description='The user email'),
    'first_name': fields.String(description='The user first name'),
    'last_name': fields.String(description='The user last name'),
    'created_at': fields.String(description='The user creation timestamp'),
    'updated_at': fields.String(description='The user update timestamp')
})

@ns_users.route('/')
class UserList(Resource):
    @ns_users.doc('list_users')
    @ns_users.marshal_list_with(user_response_model)
    def get(self):
        users = []
        data = data_manager._read_data()
        if 'Users' in data:
            users = list(data['Users'].values())
        return users, 200

    @ns_users.doc('create_user')
    @ns_users.expect(user_request_model)
    @ns_users.marshal_with(user_response_model, code=201)
    def post(self):
        data = request.get_json()
        try:
            email = data['email']
            first_name = data['first_name']
            last_name = data['last_name']
            password = data['password']

            if not (email and first_name and last_name):
                api.abort(400, "Email, first name, and last name are required.")

            existing_user = data_manager.get_by_field('email', email, 'Users')
            if existing_user:
                api.abort(409, "Email already exists.")

            user = Users(email, first_name, last_name, password)
            data_manager.save(user)
            return user.to_dict(), 201

        except KeyError:
            api.abort(400, "Invalid input format.")


@ns_users.route('/<string:user_id>')
@ns_users.response(404, 'User not found')
@ns_users.param('user_id', 'The user identifier')
class User(Resource):
    @ns_users.doc('get_user')
    @ns_users.marshal_with(user_response_model)
    def get(self, user_id):
        user = data_manager.get(user_id, 'Users')
        if user:
            return user, 200
        else:
            api.abort(404, "User not found.")

    @ns_users.doc('update_user')
    @ns_users.expect(user_request_model)
    @ns_users.marshal_with(user_response_model)
    def put(self, user_id):
        data = request.get_json()
        try:
            user = data_manager.get(user_id, 'Users')
            if not user:
                api.abort(404, "User not found.")
            
            updated_user = Users(
                email=data.get('email', user['email']),
                first_name=data.get('first_name', user['first_name']),
                last_name=data.get('last_name', user['last_name']),
            )

            updated_user.id = user_id

            data_manager.update(updated_user)
            return updated_user.to_dict(), 200

        except KeyError:
            api.abort(400, "Invalid input format.")

    @ns_users.doc('delete_user')
    @ns_users.response(204, 'User deleted')
    def delete(self, user_id):
        user = data_manager.get(user_id, 'Users')
        if not user:
            api.abort(404, "User not found.")

        data_manager.delete(user_id, 'Users')
        return '', 204


if __name__ == '__main__':
    app.run(debug=True)
