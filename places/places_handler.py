from __future__ import absolute_import

import requests
import json
from igraph import *fo

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

    @staticmethod
    def get_list_of_places(intermediate_points, types, query):
        for point in intermediate_points:
            url = PlacesHandler.BASE_URL.format(point['lat'],
                                                point['lon'],
                                                point['radius'],
                                                types,
                                                query,
                                                PlacesHandler.API_KEY)

        return json.load(requests.get(url).text)

    @staticmethod
    def find_itinerary(top_choices):
        location_graph = PlacesHandler.generate_location_graph(top_choices)


    @staticmethod
    def generate_location_graph(top_choices, start_location, end_location):
        num_vertices = len(top_choices)+2
        location_graph = Graph.Full(num_vertices)
        name_list = [start_location['name']]
        for i in xrange(1,num_vertices-1):
            name_list.append(top_choices['name'])
        name_list.append(end_location['name'])
        location_graph.vs['name'] = name_list
        location_graph.vs['name'][num_vertices - 1] = end_location['name']
        for edge in graph.es:
            location_graph.vs[edge.source]["name"]



