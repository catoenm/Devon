from __future__ import absolute_import

import requests
import json

class PlacesHandler:
    def __init__(self):
        pass

    BASE_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&types={}&name={}&key={}'
    API_KEY = 'AIzaSyDlrIrVqogcMFId9Lgzb3mkF38nXBjRszs'

    @staticmethod
    def get_places_around_me(lat, lon, radius, types):
        url = PlacesHandler.BASE_URL.format(lat,
                                            lon,
                                            radius,
                                            types,
                                            '',
                                            PlacesHandler.API_KEY)
        print url

        return json.loads(requests.get(url).text)['results']
