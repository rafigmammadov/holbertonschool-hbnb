#!/usr/bin/python3
"""
Module that contains City Model
"""
from entity import Entity
import json


class City(Entity):
    def __init__(self, country, name):
        super.__init__()
        self.country = country
        self.name = name

    def __repr__(self):
        return (f"City(country={self.country}, name='{self.name}')")

    def save(self):
        try:
            # Load existing data from the file
            with open('data.json', 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}  # If file not found, start with an empty dictionary

        # Get the list of users, or initialize an empty list if not present
        city = data.get('city', [])

        # Convert the current user instance to a dict and add it to the list
        city.append(self.to_dict())

        # Update the data dictionary with the new list of places
        data['city'] = city

        # Save the updated data back to the file
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'country': self.country,
            'name': self.name
        })
        return data
