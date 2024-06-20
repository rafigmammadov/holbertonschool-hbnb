#!/usr/bin/python3
"""
Module that contains Users Model
"""
from entity import Entity
import json


class Users(Entity):
    def __init__(self, email, first_name, last_name, password):
        super.__init__()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

    def __repr__(self):
        return (f"Users(id={self.id}, email='{self.email}'"
                f"first_name='{self.first_name}', "
                f"last_name='{self.last_name}', password={self.password})")

    def save(self):
        try:
            # Load existing data from the file
            with open('data.json', 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}  # If file not found, start with an empty dictionary

        # Get the list of users, or initialize an empty list if not present
        users = data.get('users', [])

        # Convert the current user instance to a dict and add it to the list
        users.append(self.to_dict())

        # Update the data dictionary with the new list of places
        data['users'] = users

        # Save the updated data back to the file
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'password': str(self.password),
        })
        return data
    
