from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from Model.users import Users
from Persistence.data_manager import DataManager

app = Flask(__name__)
api = Api(app, version='1.0', title='User API',
          description='A simple User API')

ns = api.namespace('users', description='User operations')

data_manager = DataManager("database.json")

user_model = api.model('User', {
    'email': fields.String(required=True, description='The user email'),
    'first_name': fields.String(required=True, description='The user first name'),
    'last_name': fields.String(required=True, description='The user last name'),
    'password': fields.String(required=True, description='The user password')
})

@ns.route('/')
class UserList(Resource):
    @ns.doc('list_users')
    @ns.marshal_list_with(user_model)
    def get(self):
        users = []
        data = data_manager._read_data()
        if 'Users' in data:
            users = list(data['Users'].values())
        return users, 200

    @ns.doc('create_user')
    @ns.expect(user_model)
    @ns.marshal_with(user_model, code=201)
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


@ns.route('/<string:user_id>')
@ns.response(404, 'User not found')
@ns.param('user_id', 'The user identifier')
class User(Resource):
    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    def get(self, user_id):
        user = data_manager.get(user_id, 'Users')
        if user:
            return user, 200
        else:
            api.abort(404, "User not found.")

    @ns.doc('update_user')
    @ns.expect(user_model)
    @ns.marshal_with(user_model)
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
                password=data.get('password', user['password']),
            )

            updated_user.id = user_id

            data_manager.update(updated_user)
            return updated_user.to_dict(), 200

        except KeyError:
            api.abort(400, "Invalid input format.")

    @ns.doc('delete_user')
    @ns.response(204, 'User deleted')
    def delete(self, user_id):
        user = data_manager.get(user_id, 'Users')
        if not user:
            api.abort(404, "User not found.")

        data_manager.delete(user_id, 'Users')
        return '', 204


if __name__ == '__main__':
    app.run(debug=True)
