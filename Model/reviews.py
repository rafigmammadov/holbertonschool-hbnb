#!/usr/bin/python3
"""
Module that contains Reviews Model
"""
from .entity import Entity
import json


class Reviews(Entity):
    def __init__(self, place_id, user_id, rating, comment):
        super.__init__()
        self.place_id = place_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment

    def __repr__(self):
        return (f"Reviews(id={self.id}, place_id='{self.place_id}'"
                f"user_id='{self.user_id}', "
                f"rating='{self.rating}', comment={self.comment})")

    def save(self):
        try:
            # Load existing data from the file
            with open('data.json', 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}  # If file not found, start with an empty dictionary

        # Get the list of users, or initialize an empty list if not present
        reviews = data.get('reviews', [])

        # Convert the current user instance to a dict and add it to the list
        reviews.append(self.to_dict())

        # Update the data dictionary with the new list of places
        data['reviews'] = reviews

        # Save the updated data back to the file
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'place_id': str(self.place_id),
            'user_id': str(self.user_id),
            'rating': self.rating,
            'comment': self.comment,
        })
        return data
