#!/usr/bin/python3
"""
Module that contains Amenity Model
"""
from .entity import Entity
import json


class Amenity(Entity):
    def __init__(self, name, description):
        super().__init__()
        self.name = name
        self.description = description

    def __repr__(self):
        return (f"Amenity(name={self.name}, description='{self.description}')")

    def save(self):
        try:
            # Load existing data from the file
            with open('data.json', 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}  # If file not found, start with an empty dictionary

        # Get the list of users, or initialize an empty list if not present
        amenity = data.get('amenity', [])

        # Convert the current user instance to a dict and add it to the list
        amenity.append(self.to_dict())

        # Update the data dictionary with the new list of places
        data['amenity'] = amenity

        # Save the updated data back to the file
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'name': self.name,
            'description': self.description
        })
        return data
