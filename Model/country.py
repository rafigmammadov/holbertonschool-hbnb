#!/usr/bin/python3
"""
Module that contains Country Model
"""
import json

def load_iso_3166_1_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

iso_3166_1_data = load_iso_3166_1_data('iso_3166_1.json')



class Country:
    def __init__(self, name, country_code):
        if country_code not in iso_3166_1_data:
            raise ValueError(f"Invalid country code: {country_code}")

        self.name = name
        self.country_code = iso_3166_1_data[country_code]
        self.cities = []

    def add_city(self, city):
        self.cities.append(city)

    def __repr__(self):
        return (f"Country(name={self.name}, cities={self.cities})")
