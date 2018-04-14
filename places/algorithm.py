from __future__ import absolute_import

import requests
import json
from igraph import *
from places.intermediate_places import IntermediatePlaces

class GoogleDistanceMatrix():
    BASE_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={},{}&destinations={},{}&key={}'
    API_KEY = 'AIzaSyDlrIrVqogcMFId9Lgzb3mkF38nXBjRszs'

class Algorithm():
    def __init__(self):
        pass

    @staticmethod
    def find_itinerary(top_choices, start_location, end_location):
        location_graph = Algorithm.generate_location_graph(top_choices, start_location, end_location)
        source = location_graph.vs.find('source')
        target = location_graph.vs.find('target')
        routes = location_graph.get_all_shortest_paths(source, target, location_graph.es['weight'], OUT)
        routes_list = []
        for idx,route in enumerate(routes):
            routes_list.append([])
            for v_id in route:
                vertex = location_graph.vs(v_id)
                route_point = {
                    'name': vertex['name'],
                    'lat': vertex['lat'],
                    'lon': vertex['lon'],
                }
                routes_list[idx].append(route_point)
        return routes_list

    @staticmethod
    def generate_location_graph(top_choices, start_location, end_location):
        num_vertices = len(top_choices ) +2
        location_graph = Graph.Full(num_vertices)
        name_list = [start_location['name']]
        lat_list = [start_location['lat']]
        lon_list = [start_location['lon']]
        id_list = [start_location['id']]
        for choice in top_choices:
            name_list.append(choice['name'])
            lat_list.append(choice['lat'])
            lon_list.append(choice['lon'])
            id_list.append(choice['id'])
        name_list.append(end_location['name'])
        lat_list.append((end_location['lat']))
        lon_list.append((end_location['lon']))
        id_list.append((end_location['id']))
        location_graph.vs['name'] = name_list
        location_graph.vs['lat'] = lat_list
        location_graph.vs['lon'] = lon_list
        location_graph.vs['id'] = id_list

        weight_list = []
        for edge in location_graph.es:
            source = location_graph.vs[edge.source]
            target = location_graph.vs[edge.target]

            if source['id'] == start_location['id'] and target['id'] == end_location['id']:
                location_graph.delete_edges(edge)
            else:
                url = GoogleDistanceMatrix.BASE_URL.format(source['lat'],
                                                           source['lon'],
                                                           target['lat'],
                                                           target['lon'],
                                                           GoogleDistanceMatrix.API_KEY)
                results = json.loads(requests.get(url).text)
                weight_list.append(results['rows'][0]['elements'][0]['duration']['value'])
        location_graph.es['weight'] = weight_list
        return location_graph

    @staticmethod
    def run():
        start_location = {'name': 'source', 'lat': 37.802798, 'lon': -122.475276, 'id': 'none'}
        end_location = {'name': 'target', 'lat': 37.740380, 'lon': -122.392192, 'id': 'none'}
        # top_choices = IntermediatePlaces.places_between_pings(37.802798, -122.475276, 37.740380, -122.392192, 5)
        top_choices = [{'lat': 37.7831952, 'lon': -122.4617746, 'name': u"Grain D'Or", 'id': u'12589d284df20ba6da644ed39a317371c6282003'}, {'lat': 37.7818872, 'lon': -122.4911466, 'name': u'Saltroot Caf\xe9', 'id': u'58db40a0d01c362c4ccab95c07553e65d0350968'}, {'lat': 37.7822418, 'lon': -122.4829307, 'name': u'Four Star Theatre', 'id': u'65df7a8e444e72ea7ad73ee78e4870df51843962'}, {'lat': 37.7814126, 'lon': -122.4606499, 'name': u'LITTLE SWEET', 'id': u'e4cacc942811a657699c4515b7eb3870f38d763b'}, {'lat': 37.7810339, 'lon': -122.4858834, 'name': u'ABC Aquatic', 'id': u'0fc6965bd36d318505a5eb7519e70b2f567bdf18'}]
        routes = Algorithm.find_itinerary(top_choices, start_location, end_location)
        print(routes)
