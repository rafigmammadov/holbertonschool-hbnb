#!/usr/bin/python3
"""
Base class for all entities in the application. This class provides
common attributes and methods that are shared across different models.

Attributes:
    id (UUID): A unique identifier for the entity, generated using UUID4 to ensure global uniqueness.
    created_at (datetime): The timestamp when the entity was created.
    updated_at (datetime): The timestamp when the entity was last updated.
"""
import uuid
from datetime import datetime, timezone

class Entity:
    def __init__(self):
        self.id = uuid.uuid4()  # Generate a new UUID for the entity
        self.created_at = datetime.now(timezone.utc)  # Store the current UTC time as creation time
        self.updated_at = datetime.now(timezone.utc)  # Store the current UTC time as update time

    def save(self):
        """
        Placeholder save method. This method should be overridden in subclasses
        to provide functionality for saving the entity to a persistent storage.
        """
        raise NotImplementedError("The save method should be implemented by subclasses")

    def to_dict(self):
        """
        Converts the Entity instance to a dictionary representation.

        Returns:
            dict: A dictionary containing the entity's data.
        """
        return {
            'id': str(self.id),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

