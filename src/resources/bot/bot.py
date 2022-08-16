import os
import json
from dotenv import load_dotenv
import requests
from flask import request, Blueprint
from twilio.twiml.messaging_response import MessagingResponse
from src.resources.locations.locations import get_location_by_phone
from src.resources.quotes.quotes import post_quote, get_quote_by_phone

load_dotenv()
bot_resource = Blueprint('bot', __name__, template_folder='templates')


@bot_resource.route('/bot', methods=['POST'])
def bot() -> str:
    incoming_msg = request.values
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    phone_number = incoming_msg['From']
    location = get_location_by_phone(phone_number.split("+")[1])
    if location:    
        if ('Latitude' in incoming_msg) and ('Longitude' in incoming_msg):
            object_distance_calc = get_distance(
                {'latitude': str(location['lat']), 'longitude': str(location['long'])},
                {'latitude': incoming_msg['Latitude'], 'longitude': incoming_msg['Longitude']}
            )
            if object_distance_calc["status"] == 'OK':
                distance = object_distance_calc['distance']
                duration = object_distance_calc['duration']
                cost = get_cost(distance, location['tax_min'],
                                location['tax_max'], location['tax_extra'])
                response = bot_responses('success').format(
                    location['name'], distance, duration, str(cost))
            else:
                response = bot_responses('error').format(location['name'])
            msg.body(response)
            responded = True
        if not responded:
            msg.body(bot_responses('no_shipping_location').format(location['name']))
        return str(resp)
    else:
        quote = get_quote_by_phone(phone_number.split("+")[1])
        if quote['status'] == 'ok':
            msg.body(bot_responses('no_location'))
        else:
            msg.body(bot_responses('no_origin_location'))
        return str(resp)


def get_distance(origin_coords:object , destination_coords:object) -> object:
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
            'message': 'Hola {}.\nLa distacia de tu envío es: {}.\nEl tiempo aproximado de entrega es: {}.\nEl costo será de: ${}'
            ' pesos.'
        },
        {
            'type': 'error',
            'message': 'Hola {}, no se pudo calcular el costo, envia nuevamente '
            'la ubicación'
        },
        {
            'type': 'no_shipping_location',
            'message': 'Hola {} envia la ubicación de destino de tu envío para calcular el costo de entrega.'
        },
        {
            'type': 'no_origin_location',
            'message': 'Bienvenido al cotizador de Devolada, por favor ingresa primero la ubicación donde debemos recoger tu paquete.'
        }
    ]
    for x in responses:
        if x['type'] == type:
            return x['message']
