from __future__ import absolute_import

import random


class PlaceTypes:
    TYPES = ['amusement_park',
             'aquarium',
             'art_gallery',
             'bakery',
             'bar',
             'beauty_salon',
             'bicycle_store',
             'book_store',
             'bowling_alley',
             'cafe',
             'campground',
             'casino',
             'city_hall',
             'clothing_store',
             'liquor_store',
             'movie_rental',
             'movie_theater',
             'moving_company',
             'museum',
             'night_club',
             'park',
             'post_office',
             'restaurant',
             'shopping_mall',
             'spa',
             'stadium',
             'travel_agency',
             'zoo',
             'food']

    def __init__(self):
        pass

    @staticmethod
    def serve_types(num_places):
        return random.sample(PlaceTypes.TYPES, num_places)
