import unittest
from Model.country import Country

class TestCountry(unittest.TestCase):

    def test_country_initialization(self):
        country_name = "Test Country"
        country = Country(country_name)


        self.assertEqual(country.name, country_name)
        self.assertEqual(country.cities, [])

    def test_add_city(self):
        country = Country("Test Country")
        city_name = "Test City"
        country.add_city(city_name)


        self.assertIn(city_name, country.cities)

    def test_repr(self):
        country_name = "Test Country"
        country = Country(country_name)


        expected_repr = f"Country(name={country_name}, cities=[])"
        self.assertEqual(repr(country), expected_repr)

if __name__ == '__main__':
    unittest.main()


