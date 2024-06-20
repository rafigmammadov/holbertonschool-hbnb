#!/usr/bin/python3
"""
Module that contains Country Model
"""
import json


class Country:
    def __init__(self, name, cities):
        self.name = name
        self.cities = []

    def add_city(self, city):
        self.cities.append(city)

    def __repr__(self):
        return (f"Country(name={self.name}, cities={self.cities})")