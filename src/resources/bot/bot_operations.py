import os
import json
import requests
from datetime import datetime
from src.resources.quotes.quotes import save_quote


class BotOperations:

    def __init__(self, responses) -> None:
        self.responses = responses


    def calculate_cost_to_location(self, phone: int, location: object, incoming_msg: object, quote_status: str) -> object:
        quote = {'phone': phone, 'lat': float(location['lat']), 'long': float(location['long']),
                 'shipping_location': {'lat': float(incoming_msg['Latitude']), 'long': float(incoming_msg['Longitude'])},
                 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow(), 'quote_status': str(quote_status),
                 'tax_min': int(location['tax_min']), 'tax_extra': int(location['tax_extra']),
                 'tax_max': int(location['tax_max']), 'is_location': bool(True), 'status': bool(True)}
        saving_quote = save_quote(quote)
        if saving_quote['status'] == 'ok':
            response = self.calculate_cost(location, incoming_msg)
        else:
            response = self.responses('error_save_shipping_location')
        return response


    def calculate_cost(self, location, incoming_msg):
        location_coordinates = {'latitude': str(
            location['lat']), 'longitude': str(location['long'])}
        location_taxes = {
            'tax_min': location['tax_min'], 'tax_max': location['tax_max'], 'tax_extra': location['tax_extra']}
        shipping_coordinates = {
            'latitude': incoming_msg['Latitude'], 'longitude': incoming_msg['Longitude']}
        distance, duration, cost = BotOperations.get_shipping_variables(self, 
            location_coordinates, shipping_coordinates, location_taxes)
        if distance:
            response = self.responses('success').format(
                distance, duration, str(cost))
        else:
            response = self.self.responses('error').format(location['name'])
        return response


    def get_shipping_variables(self, location_coordinates: object, shipping_coordinates: object, location_taxes: object):
        object_distance_calc = BotOperations.get_distance(
            location_coordinates, shipping_coordinates)
        if object_distance_calc["status"] == 'OK':
            distance = object_distance_calc['distance']
            duration = object_distance_calc['duration']
            cost = BotOperations.get_monetary_cost(
                distance, location_taxes['tax_min'], location_taxes['tax_max'], location_taxes['tax_extra'])
            return distance, duration, cost


    def get_distance(origin_coords: object, destination_coords: object) -> object:
        url = ("{}origins={}%2C{}&destinations={}%2C{}&key={}")
        url = url.format(os.environ.get("MAPS_URI"),
                         origin_coords['latitude'], origin_coords['longitude'],
                         destination_coords['latitude'],
                         destination_coords['longitude'],
                         os.environ.get("GOOGLE_MAPS_API_KEY"))
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        response_json = json.loads(response.text)
        object_response = {
            'status': response_json['status'],
            'distance': response_json["rows"][0]["elements"][0]["distance"]["text"],
            'duration': response_json["rows"][0]["elements"][0]["duration"]["text"]
        }
        return object_response


    def get_monetary_cost(distance: str, tax_min: int, tax_max: int, tax_extra: int) -> float:
        distance = distance.split(" ")
        if distance[1] == 'm':
            return tax_min
        elif distance[1] == 'km':
            if float(distance[0]) <= 2.5:
                cost = tax_min
            elif float(distance[0]) > 2.5 and float(distance[0]) <= 5:
                cost = tax_max
            else:
                cost = ((float(distance[0]) - float(5)) * tax_extra) + tax_max
            return cost
