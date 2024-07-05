from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .city import City  # Assuming City model is defined in city.py

Base = declarative_base()

class Country(Base):
    __tablename__ = 'countries'

    country_code = Column(String(2), primary_key=True)
    name = Column(String(255), nullable=False)

    cities = relationship("City", back_populates="country")

    def __init__(self, country_code, name):
        self.country_code = country_code
        self.name = name

    def __repr__(self):
        return f"<Country(country_code={self.country_code}, name='{self.name}')>"

    def add_city(self, city):
        self.cities.append(city)

    def to_dict(self):
        return {
            'country_code': self.country_code,
            'name': self.name,
            'cities': [city.to_dict() for city in self.cities]
        }

