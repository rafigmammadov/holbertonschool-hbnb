from Persistence.persistance_manager import IPersistenceManager
import os
import json
from uuid import UUID

class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)

class DataManager(IPersistenceManager):
    def __init__(self, filename="database.json"):
        self.filename = filename

        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                json.dump({}, file)

    def _read_data(self):
        try:
            with open(self.filename, 'r', encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def _write_data(self, data):
        with open(self.filename, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=4, cls=UUIDEncoder)  # Use custom encoder here

    def save(self, entity):
        data = self._read_data()
        entity_type = type(entity).__name__
        entity_id = str(getattr(entity, 'id', None))

        if entity_type not in data:
            data[entity_type] = {}

        data[entity_type][entity_id] = entity.__dict__
        self._write_data(data)

    def get(self, entity_id, entity_type):
        data = self._read_data()
        entity_id = str(entity_id)
        if entity_type in data and entity_id in data[entity_type]:
            return data[entity_type][entity_id]

        return None

    def update(self, entity):
        data = self._read_data()
        entity_type = type(entity).__name__
        entity_id = str(getattr(entity, 'id', None))

        if entity_type in data and entity_id in data[entity_type]:
            data[entity_type][entity_id] = entity.__dict__
            self._write_data(data)
        else:
            raise ValueError(f"Entity of type {entity_type} "
                             f"with id {entity_id} not found")

    def delete(self, entity_id, entity_type):
        data = self._read_data()
        entity_id = str(entity_id)

        if entity_type in data and entity_id in data[entity_type]:
            del data[entity_type][entity_id]

            if not data[entity_type]:
                del data[entity_type]
            self._write_data(data)
        else:
            raise ValueError(f"Entity of type {entity_type} "
                             f"with id {entity_id} not found")
