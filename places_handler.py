from __future__ import absolute_import

import requests


class PlacesHandler(object):
    BASE_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&types={}&name={}&key={}'
    API_KEY = 'AIzaSyDlrIrVqogcMFId9Lgzb3mkF38nXBjRszs'

    @staticmethod
    def get_places_around_me(lat, lon, radius, types, name):
        url = PlacesHandler.BASE_URL.format(lat,
                                            lon,
                                            radius,
                                            types,
                                            name,
                                            PlacesHandler.API_KEY)
        return requests.get(url).text

