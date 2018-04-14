from __future__ import absolute_import
from places_handler import PlacesHandler

# API Key: AIzaSyDlrIrVqogcMFId9Lgzb3mkF38nXBjRszs

response = PlacesHandler.get_places_around_me(-33.8670,
                                         151.1957,
                                         500,
                                         'food',
                                         'cruise')

print response
