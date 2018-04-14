from __future__ import absolute_import

import geopy.distance
import random
from places.places_handler import PlacesHandler
from places.place_types import PlaceTypes


class Circle(object):
    def __init__(self, lat, lon, rad):
        self._lat = lat
        self._lon = lon
        self._rad = rad

    @property
    def lat(self):
        return self._lat

    @property
    def lon(self):
        return self._lon

    @property
    def rad(self):
        return self._rad


class IntermediatePlaces():
    def __init__(self):
        pass

    @staticmethod
    def sort_places_by_rating(place_list):
        sort_by = 'rating'
        sorted_list = [(item[sort_by], item) for item in place_list]
        sorted_list.sort()
        result = [item for (_, item) in sorted_list]
        return result

    @staticmethod
    def distance_between_pings(lat_1, lon_1,
                               lat_2, lon_2):
        """Returns the distance between two pings"""

        coords_1 = (lat_1, lon_1)
        coords_2 = (lat_2, lon_2)
        return geopy.distance.vincenty(coords_1, coords_2).m

    @staticmethod
    def path_circles(lat_1, lon_1,
                     lat_2, lon_2,
                     num_circles):
        """Returns N path circles from one coordinate to another"""

        lat_incr = (lat_1 - lat_2) / float(num_circles)
        lon_incr = (lon_1 - lon_2) / float(num_circles)
        radius = IntermediatePlaces.distance_between_pings(lat_1, lon_1, lat_2, lon_2) / float(num_circles)

        path_circles = []
        curr_lat = lat_1
        curr_lon = lon_1
        for circle in xrange(num_circles):
            path_circles.append(Circle(curr_lat, curr_lon, radius))
            curr_lat += lat_incr
            curr_lon += lon_incr

        return path_circles

    @staticmethod
    def places_between_pings(lat_1, lon_1,
                             lat_2, lon_2,
                             num_places):
        """Returns a list of places to visit between pings"""

        path_circles = IntermediatePlaces.path_circles(lat_1, lon_1,
                                                       lat_2, lon_2,
                                                       3)
        types = PlaceTypes.serve_types(num_places)

        places = []
        for circle in path_circles:
            for type in types:
                # Make request to Google places API
                response = PlacesHandler.get_places_around_me(circle.lat,
                                                              circle.lon,
                                                              circle.rad,
                                                              type)
                for place in response:
                    places.append({'name':   place['name'],
                                   'lat':    place['geometry']['location']['lat'],
                                   'lon':    place['geometry']['location']['lng'],
                                   'id':     place['id']})
        random.shuffle(places)
        return places[-num_places:]


if __name__ == '__main__':
    print IntermediatePlaces.places_between_pings(37.802798, -122.475276,
                                                  37.740380, -122.392192,
                                                  5)
