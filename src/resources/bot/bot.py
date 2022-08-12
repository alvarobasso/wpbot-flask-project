from flask import request, Blueprint
from twilio.twiml.messaging_response import MessagingResponse
import requests
from src.resources.locations.locations import get_location_by_phone

bot_resource = Blueprint('bot', __name__,template_folder='templates')

@bot_resource.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values
    resp = MessagingResponse()
    msg = resp.message()
    responded = False 
    phone_number = incoming_msg['From']
    location_data = get_location_by_phone(phone_number.split("+")[1])
    if location_data:
        location_name = location_data['name']
        location_latitude = str(location_data['lat'])
        location_longitude = str(location_data['long'])

    if ('Latitude' in incoming_msg) and ('Longitude' in incoming_msg): 
        list_distance_calc = get_distance(
                {'latitude':location_latitude, 'longitude':location_longitude},
                {'latitude':incoming_msg['Latitude'], 'longitude':incoming_msg['Longitude']}
                )
        if list_distance_calc["status"] == 'OK':
            
            cost = list_distance_calc["rows"][0]["elements"][0]["distance"]["text"].split(" ", 1)[0]
            cost = float(cost) * 10
            distance = list_distance_calc["rows"][0]["elements"][0]["distance"]["text"]
            duration = list_distance_calc["rows"][0]["elements"][0]["duration"]["text"]

            response = ('Hola {}, la distacia de tu envío es de: '
            '{}, el tiempo aprox. del viaje es de: {}. El costo será de: {}'
            ' pesos.').format(location_name,distance, duration, str(cost))	
        else :
            response = ('Hola {}, no se pudo calcular el costo, envia nuevamente '
                        'la ubicación').format(location_name)
        msg.body(response)
        responded = True
    if not responded:
        msg.body(("Hola {} envia la ubicación de destino de tu envío para calcular "
                "el costo de entrega.").format(location_name))
        #msg.body(response)
    return str(resp)


def get_distance(origin_coords, destination_coords):
    path = ("https://maps.googleapis.com/maps/api/distancematrix/json?"
    "origins={}%2C{}&destinations={}%2C{}&key=AIzaSyCKczNTPCKd3rE9oiyJ6WqP-W6qCT51eg0").format(origin_coords['latitude'],origin_coords['longitude'],
    destination_coords['latitude'],destination_coords['longitude'])
    url = path
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()