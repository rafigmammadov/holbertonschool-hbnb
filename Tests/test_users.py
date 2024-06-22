# tests/test_users.py
import unittest
import os
import json
from Model.users import Users

class TestUsers(unittest.TestCase):

    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'secure_password'
        }

    def tearDown(self):
        if os.path.exists('data.json'):
            os.remove('data.json')

    def test_save_user(self):
        user = Users(**self.user_data)
        user.save()


        self.assertTrue(os.path.exists('data.json'))


        with open('data.json', 'r') as f:
            data = json.load(f)
            self.assertIn('users', data)
            self.assertEqual(len(data['users']), 1)

            saved_user = data['users'][0]
            self.assertEqual(saved_user['email'], 'test@example.com')
            self.assertEqual(saved_user['first_name'], 'John')
            self.assertEqual(saved_user['last_name'], 'Doe')
            self.assertEqual(saved_user['password'], 'secure_password')

if __name__ == '__main__':
    unittest.main()

