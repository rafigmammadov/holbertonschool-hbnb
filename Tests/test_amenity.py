import unittest
import json
from unittest.mock import patch, mock_open
from Model.amenity import Amenity

class TestAmenity(unittest.TestCase):

    def setUp(self):
        self.amenity = Amenity("AmenityName", "AmenityDescription")

    def test_init(self):
        self.assertEqual(self.amenity.name, "AmenityName")
        self.assertEqual(self.amenity.description, "AmenityDescription")

    def test_repr(self):
        expected_repr = "Amenity(name=AmenityName, description='AmenityDescription')"
        self.assertEqual(repr(self.amenity), expected_repr)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save(self, mock_json_dump, mock_open):

        mock_open.return_value = mock_open(read_data='{"amenity": []}')


        self.amenity.save()


        call_args = mock_json_dump.call_args
        if call_args:
            _, kwargs = call_args
            dumped_data = kwargs['obj']
            self.assertIn('amenity', dumped_data)
            self.assertEqual(len(dumped_data['amenity']), 1)

if __name__ == '__main__':
    unittest.main()


