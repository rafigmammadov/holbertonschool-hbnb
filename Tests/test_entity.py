import unittest
from Model.entity import Entity

class TestEntity(unittest.TestCase):

    def test_entity_initialization(self):
        entity = Entity()


        self.assertTrue(isinstance(entity.id, uuid.UUID))


        self.assertIsInstance(entity.created_at, datetime)
        self.assertIsInstance(entity.updated_at, datetime)


        self.assertAlmostEqual(entity.created_at, entity.updated_at, delta=timedelta(seconds=1))

    def test_to_dict(self):
        entity = Entity()
        entity_dict = entity.to_dict()


        self.assertIn('id', entity_dict)
        self.assertIn('created_at', entity_dict)
        self.assertIn('updated_at', entity_dict)


        self.assertTrue(isinstance(entity_dict['id'], str))
        self.assertTrue(uuid.UUID(entity_dict['id']))


        try:
            datetime.fromisoformat(entity_dict['created_at'])
            datetime.fromisoformat(entity_dict['updated_at'])
        except ValueError:
            self.fail("created_at or updated_at is not in ISO 8601 format")

if __name__ == '__main__':
    unittest.main()


