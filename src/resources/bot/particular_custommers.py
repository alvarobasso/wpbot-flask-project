from datetime import datetime
from urllib import response
from src.resources.quotes.quotes import save_quote, update_quote, get_quote_by_phone, get_quote_by_id
from src.resources.bot.bot_operations import BotOperations
from src.notifications.notifications import send_whats_app_notification, send_whats_app_location
from src.utils.objects import Objects
from src.utils.strings import Strings


class ParticularCustomers:

    def __init__(self, responses) -> None:
        self.responses = responses
        self.bot_operations = BotOperations(responses)
        self.objects = Objects()
        self.strings = Strings()

    def send_notification(self, id_quote: str):
        quote = get_quote_by_id(id_quote)
        quote_id = str(quote['_id'])
        quote_id = quote_id[-5:]
        location_coordinates = self.objects.object_coordinates(
            quote['lat'], quote['long'])
        location_taxes = self.objects.object_taxes(
            quote['tax_min'], quote['tax_max'], quote['tax_extra'])
        shipping_coordinates = self.objects.object_coordinates(
            quote['shipping_location']['lat'], quote['shipping_location']['long'])
        distance, duration, cost = self.bot_operations.get_shipping_variables(
            location_coordinates, shipping_coordinates, location_taxes)
        location_coords = self.strings.location_coordenates(
            quote['lat'], quote['long'])
        location_message = self.strings.location_message(
            quote_id, ' - Ubicación paquete')
        shipping_coords = str(
            quote['shipping_location']['lat'])+','+str(quote['shipping_location']['long'])
        shipping_message = self.strings.location_message(
            quote_id, ' - Ubicación entrega')
        message = self.responses('particular_quoted').format(
            quote_id, quote['phone'], cost, distance, duration)
        send_whats_app_notification('+5217774386474', message)
        send_whats_app_location(
            '+5217774386474', location_message, location_coords)
        send_whats_app_location(
            '+5217774386474', shipping_message, shipping_coords)

    def particular_quote(self, phone_number: int, incoming_msg: object) -> object:
        quote = get_quote_by_phone(phone_number)
        if quote['status'] == 'ok' and quote['quote_status'] == 'pending':
            if ('Latitude' in incoming_msg) and ('Longitude' in incoming_msg):
                return self.calculate_cost_to_particular(
                    phone_number, incoming_msg, 'quoted', quote)
            else:
                return (self.responses('no_shipping_location'))
        if quote['status'] == 'ok' and quote['quote_status'] == 'quoted':
            return (self.responses('pendding_quoted'))
        else:
            if ('Latitude' in incoming_msg) and ('Longitude' in incoming_msg):
                return self.calculate_cost_to_particular(
                    phone_number, incoming_msg, 'pending', quote)
            else:
                return self.responses('no_origin_location')

    def calculate_cost_to_particular(self, phone: int, incoming_msg: object, quote_status: str, quote: object) -> object:
        if quote_status == 'pending':
            quote = {'phone': phone, 'lat': float(incoming_msg['Latitude']), 'long': float(incoming_msg['Longitude']),
                     'shipping_location': {'lat': float(0), 'long': float(0)},
                     'created_at': datetime.utcnow(),
                     'updated_at': datetime.utcnow(), 'quote_status': str(quote_status),
                     'tax_min': int(35), 'tax_extra': int(10), 'tax_max': int(50), 'is_location': bool(False), 'status': bool(True)}
            saving_quote = save_quote(quote)
            if saving_quote['status'] == 'ok':
                response = self.responses('save_origin_location')
            else:
                response = self.responses('error_save_origin_location')
            return response
        elif quote_status == 'quoted':
            quote_data = {'phone': phone, 'shipping_location': {'lat': incoming_msg['Latitude'], 'long': incoming_msg['Longitude']},
                          'updated_at': datetime.utcnow(), 'quote_status': quote_status, 'status': True}
            updating_quote = update_quote(quote_data)
            if updating_quote['status'] == 'ok':
                response = self.bot_operations.calculate_cost(
                    quote, incoming_msg)
            else:
                response = self.responses('error_save_origin_location')
            return response
