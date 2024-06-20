import unittest
import json
from unittest.mock import patch, mock_open
from Model.city import City

class TestCity(unittest.TestCase):

    def setUp(self):
        self.city = City("CountryName", "CityName")

    def test_init(self):
        self.assertEqual(self.city.country, "CountryName")
        self.assertEqual(self.city.name, "CityName")

    def test_repr(self):
        expected_repr = "City(country=CountryName, name='CityName')"
        self.assertEqual(repr(self.city), expected_repr)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save(self, mock_json_dump, mock_open):

        mock_open.return_value = mock_open(read_data='{"city": []}')


        self.city.save()


        call_args = mock_json_dump.call_args
        if call_args:
            _, kwargs = call_args
            dumped_data = kwargs['obj']
            self.assertIn('city', dumped_data)
            self.assertEqual(len(dumped_data['city']), 1)

if __name__ == '__main__':
    unittest.main()


