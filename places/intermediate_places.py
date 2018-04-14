from __future__ import absolute_import

from places.places_handler import PlacesHandler


class IntermediatePlaces():
    @staticmethod
    def get_places_between_pings(lat_1,
                                 lon_1,
                                 lat_2,
                                 lon_2,
                                 radius,
                                 types,
                                 name):
        # TODO: make this actually work
        response = PlacesHandler.get_places_around_me(lat_1,
                                                      lon_1,
                                                      radius,
                                                      types,
                                                      name)
        return response


print IntermediatePlaces.get_places_between_pings(-33.8670,
                                                  151.1957,
                                                  -33.8670,
                                                  151.1957,
                                                  500,
                                                  'food',
                                                  'cruise')
