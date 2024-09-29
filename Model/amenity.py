from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from app import db  # Assuming 'db' is your SQLAlchemy instance

Base = declarative_base()

class Amenity(Base):
    __tablename__ = 'amenities'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<Amenity(id={self.id}, name={self.name}, description='{self.description}')>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

