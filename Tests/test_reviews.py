import unittest
from Model.reviews import Reviews

class TestReviews(unittest.TestCase):

    def test_save_review(self):
        review_data = {
            'place_id': '123',
            'user_id': '456',
            'rating': 4.5,
            'comment': 'Nice place!'
        }
        review = Reviews(**review_data)
        review.save()



    def test_to_dict(self):
        review_data = {
            'place_id': '123',
            'user_id': '456',
            'rating': 4.5,
            'comment': 'Nice place!'
        }
        review = Reviews(**review_data)
        review_dict = review.to_dict()

        expected_dict = {
            'place_id': '123',
            'user_id': '456',
            'rating': 4.5,
            'comment': 'Nice place!'
        }

        self.assertEqual(review_dict, expected_dict)

if __name__ == '__main__':
    unittest.main()


