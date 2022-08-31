from datetime import datetime
from urllib import response
from src.resources.quotes.quotes import save_quote, update_quote, get_quote_by_phone, get_quote_by_id
from src.resources.bot.bot_operations import BotOperations
from src.notifications.notifications import send_whats_app_notification

class ParticularCustomers:

    def __init__(self, responses) -> None:
        self.responses = responses
        self.bot_operations = BotOperations(responses)


    def send_notification(self, id_quote:str):
            quote = get_quote_by_id(id_quote)
            print(quote)
            first_message = self.responses('particular_quoted_first_part').format(quote['phone'])
            first_location = str(quote['lat'])+','+str(quote['long'])
            first_notification = send_whats_app_notification('+5217774386474',first_message, first_location)
            
            second_message = self.responses('particular_quoted_second_part').format('Con un costo de...')
            second_location = str(quote['shipping_location']['lat'])+','+str(quote['shipping_location']['long'])
            second_notification = send_whats_app_notification('+5217774386474',second_message, second_location)


    def particular_quote(self, phone_number: int, incoming_msg:object) -> object:
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
                    'tax_min': int(35), 'tax_extra': int(10), 'tax_max': int(50), 'is_location':bool(False), 'status': bool(True)}
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
                response = self.bot_operations.calculate_cost(quote, incoming_msg)
            else:
                response = self.responses('error_save_origin_location')
            return response