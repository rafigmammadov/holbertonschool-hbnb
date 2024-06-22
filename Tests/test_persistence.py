import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Persistence.data_manager import DataManager

class TestEntity:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class TestDataManager(unittest.TestCase):

    def setUp(self):
        self.filename = "test_database.json"
        self.data_manager = DataManager(filename=self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_save_and_get(self):
        entity = TestEntity(id=1, name="Test Entity")
        self.data_manager.save(entity)
        retrieved_entity = self.data_manager.get(1, 'TestEntity')
        self.assertIsNotNone(retrieved_entity)
        self.assertEqual(retrieved_entity['id'], 1)
        self.assertEqual(retrieved_entity['name'], "Test Entity")

    def test_update(self):
        entity = TestEntity(id=1, name="Test Entity")
        self.data_manager.save(entity)
        entity.name = "Updated Entity"
        self.data_manager.update(entity)
        updated_entity = self.data_manager.get(1, 'TestEntity')
        self.assertIsNotNone(updated_entity)
        self.assertEqual(updated_entity['name'], "Updated Entity")

    def test_delete(self):
        entity = TestEntity(id=1, name="Test Entity")
        self.data_manager.save(entity)
        self.data_manager.delete(1, 'TestEntity')
        deleted_entity = self.data_manager.get(1, 'TestEntity')
        self.assertIsNone(deleted_entity)

    def test_get_non_existent(self):
        non_existent_entity = self.data_manager.get(999, 'TestEntity')
        self.assertIsNone(non_existent_entity)

if __name__ == '__main__':
    unittest.main()
