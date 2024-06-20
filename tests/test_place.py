import unittest
from Model.place import Place

class TestPlace(unittest.TestCase):

    def test_save_place(self):
        place_data = {
            'name': 'Cozy Apartment',
            'description': 'A comfortable apartment in the heart of the city.',
            'address': '123 Main St',
            'city_id': '789',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'host_id': '123',
            'number_of_rooms': 2,
            'bathrooms': 1,
            'price_per_night': 100,
            'max_guests': 4,
            'amenities': ['Wi-Fi', 'Kitchen']
        }
        place = Place(**place_data)
        place.save()


    def test_to_dict(self):
        place_data = {
            'name': 'Cozy Apartment',
            'description': 'A comfortable apartment in the heart of the city.',
            'address': '123 Main St',
            'city_id': '789',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'host_id': '123',
            'number_of_rooms': 2,
            'bathrooms': 1,
            'price_per_night': 100,
            'max_guests': 4,
            'amenities': ['Wi-Fi', 'Kitchen']
        }
        place = Place(**place_data)
        place_dict = place.to_dict()

        expected_dict = {
            'name': 'Cozy Apartment',
            'description': 'A comfortable apartment in the heart of the city.',
            'address': '123 Main St',
            'city_id': '789',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'host_id': '123',
            'number_of_rooms': 2,
            'bathrooms': 1,
            'price_per_night': 100,
            'max_guests': 4,
            'amenities': ['Wi-Fi', 'Kitchen']
        }

        self.assertEqual(place_dict, expected_dict)

if __name__ == '__main__':
    unittest.main()


