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
        route_points = []
        for route in enumerate(routes):
            for v_id in route:
                vertex = location_graph.vs(v_id)
                route_point = {
                    'name': vertex['name'][0],
                    'lat': vertex['lat'][0],
                    'lon': vertex['lon'][0],
                }
                route_points.append(route_point)
            break;
        return route_points

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
    def run(start, end):
        
        start_location = {'name': 'source', 'lat': start[0], 'lon': start[1], 'id': 'none'}
        end_location = {'name': 'target', 'lat': end[0], 'lon': end[1], 'id': 'none'}

        top_choices = IntermediatePlaces.places_between_pings(start[0], start[1], end[0], end[1], 5)

        routes = Algorithm.find_itinerary(top_choices, start_location, end_location)
        return routes
