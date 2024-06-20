#!/usr/bin/python3
"""
Module that contains Place Model
"""
from entity import Entity
import json


class Place(Entity):
    def __init__(self, name, description, address, city_id, latitude,
                 longitude, host_id, number_of_rooms, bathrooms,
                 price_per_night, max_guests, amenities):
        super.__init__()
        self.name = name
        self.description = description
        self.address = address
        self.city_id = city_id
        self.latitude = latitude
        self.longitude = longitude
        self.host_id = host_id
        self.number_of_rooms = number_of_rooms
        self.bathrooms = bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.amenities = amenities

    def __repr__(self):
        return (f"Place(id={self.id}, name='{self.name}'"
                f"description='{self.description}', "
                f"address='{self.address}', city_id={self.city_id}, "
                f"latitude={self.latitude}, "
                f"longitude={self.longitude}, host_id={self.host_id}, "
                f"number_of_rooms={self.number_of_rooms}, "
                f"bathrooms={self.bathrooms}, "
                f"price_per_night={self.price_per_night}, "
                f"max_guests={self.max_guests}, "
                f"amenities={self.amenities})")

    def save(self):
        try:
            # Load existing data from the file
            with open('data.json', 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}  # If file not found, start with an empty dictionary

        # Get the list of places, or initialize an empty list if not present
        places = data.get('places', [])

        # Convert the current place instance to a dict and add it to the list
        places.append(self.to_dict())

        # Update the data dictionary with the new list of places
        data['places'] = places

        # Save the updated data back to the file
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'city_id': str(self.city_id),
            'latitude': self.latitude,
            'longitude': self.longitude,
            'host_id': str(self.host_id),
            'number_of_rooms': self.number_of_rooms,
            'bathrooms': self.bathrooms,
            'price_per_night': self.price_per_night,
            'max_guests': self.max_guests,
            'amenities': self.amenities
        })
        return data
