from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from app import db  # Assuming 'db' is your SQLAlchemy instance

Base = declarative_base()

class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    country = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)

    def __init__(self, country, name):
        self.country = country
        self.name = name

    def __repr__(self):
        return f"<City(id={self.id}, country={self.country}, name='{self.name}')>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'country': self.country,
            'name': self.name
        }

