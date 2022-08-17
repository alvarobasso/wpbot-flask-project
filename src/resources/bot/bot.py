from datetime import date, datetime
import os
import json
from dotenv import load_dotenv
import requests
from flask import request, Blueprint
from twilio.twiml.messaging_response import MessagingResponse
from src.resources.locations.locations import get_location_by_phone
from src.resources.quotes.quotes import save_quote, update_quote, get_quote_by_phone

load_dotenv()
bot_resource = Blueprint('bot', __name__, template_folder='templates')


@bot_resource.route('/bot', methods=['POST'])
def bot() -> str:
    incoming_msg = request.values
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    phone_number = incoming_msg['From'].split("+")[1]
    location = get_location_by_phone(phone_number)
    if location:
        if ('Latitude' in incoming_msg) and ('Longitude' in incoming_msg):
            response = calculate_cost_to_location(location, incoming_msg)
            msg.body(response)
            responded = True
        if not responded:
            msg.body(bot_responses('no_shipping_location'))
        return str(resp)
    else:
        print(phone_number)
        quote = get_quote_by_phone(phone_number)
        print(quote)
        if quote['status'] == 'ok' and quote['quote_status'] == 'pending':
            if ('Latitude' in incoming_msg) and ('Longitude' in incoming_msg):
                response = calculate_cost_to_particular(
                    phone_number, incoming_msg, 'quoted', quote)
                msg.body(response)
                responded = True
            else:
                msg.body(bot_responses('no_shipping_location'))
        else:
            if ('Latitude' in incoming_msg) and ('Longitude' in incoming_msg):
                response = calculate_cost_to_particular(
                    phone_number, incoming_msg, 'pending', quote)
                msg.body(response)
                responded = True
            else:
                msg.body(bot_responses('no_origin_location'))
        return str(resp)


def calculate_cost_to_particular(phone: int, incoming_msg: object, quote_status: str, quote: object) -> object:
    if quote_status == 'pending':
        quote = {'phone': phone, 'lat': float(incoming_msg['Latitude']), 'long': float(incoming_msg['Longitude']),
                 'shipping_location': {'lat': 0, 'long': 0},
                 'created_at': datetime.utcnow(),
                 'updated_at': datetime.utcnow(), 'quote_status': quote_status,
                 'tax_min': 35, 'tax_extra': 10, 'tax_max': 50, 'status': True}
        saving_quote = save_quote(quote)
        if saving_quote['status'] == 'ok':
            response = bot_responses('save_origin_location')
        else:
            response = bot_responses('error_save_origin_location')
        return response
    elif quote_status == 'quoted':
        quote_data = {'phone': phone, 'shipping_location': {'lat': incoming_msg['Latitude'], 'long': incoming_msg['Longitude']},
                      'updated_at': datetime.utcnow(), 'quote_status': quote_status, 'status': True}
        updating_quote = update_quote(quote_data)
        if updating_quote['status'] == 'ok':
            print(quote)
            response = calculate_cost_to_location(quote, incoming_msg)
        else:
            response = bot_responses('error_save_origin_location')
        return response


def calculate_cost_to_location(location, incoming_msg):
    object_distance_calc = get_distance(
        {'latitude': str(location['lat']), 'longitude': str(location['long'])},
        {'latitude': incoming_msg['Latitude'], 'longitude': incoming_msg['Longitude']})
    if object_distance_calc["status"] == 'OK':
        distance = object_distance_calc['distance']
        duration = object_distance_calc['duration']
        cost = get_cost(
            distance, location['tax_min'], location['tax_max'], location['tax_extra'])
        response = bot_responses('success').format(
            distance, duration, str(cost))
    else:
        response = bot_responses('error').format(location['name'])
    return response


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


def get_cost(distance: str, tax_min: int, tax_max: int, tax_extra: int) -> float:
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


def bot_responses(type: str) -> str:
    responses = [
        {
            'type': 'success',
            'message': 'La distacia de tu envío es: {}.\nEl tiempo aproximado de entrega es: {}.\nEl costo será de: ${}'
            ' pesos.'
        },
        {
            'type': 'error',
            'message': 'Hola {}, no se pudo calcular el costo, envia nuevamente '
            'la ubicación'
        },
        {
            'type': 'no_shipping_location',
            'message': 'Envia la ubicación de destino de tu envío para calcular el costo de entrega.'
        },
        {
            'type': 'no_origin_location',
            'message': 'Bienvenido al cotizador de Devolada, por favor ingresa primero la ubicación donde debemos recoger tu paquete.'
        },
        {
            'type': 'save_origin_location',
            'message': 'Gracias ahora envía la ubicación a donde quieres mandar tu paquete.'
        },
        {
            'type': 'error_save_origin_location',
            'message': 'Hubo un problema al registrar tu ubicación de origen, por favor intenta nuevamente.'
        }
    ]
    for x in responses:
        if x['type'] == type:
            return x['message']
