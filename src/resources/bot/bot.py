from dotenv import load_dotenv
from flask import request, Blueprint
from twilio.twiml.messaging_response import MessagingResponse
from src.resources.quotes.quotes import save_quote, update_quote, get_quote_by_phone
from src.resources.locations.locations import get_location_by_phone
from src.utils.responses import BotResponses
from src.resources.bot.bot_operations import BotOperations
from src.resources.bot.particular_custommers import ParticularCustomers

load_dotenv()
bot_resource = Blueprint('bot', __name__, template_folder='templates')

responses = BotResponses.responses
bot_operations = BotOperations(responses)
particular_customers = ParticularCustomers(responses)

@bot_resource.route('/bot', methods=['POST'])
def bot() -> str:
    incoming_msg = request.values
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    phone_number = incoming_msg['From'].split("+")[1]
    location = get_location_by_phone(phone_number)
    if incoming_msg['Body'] == 'Confirmar':
        quote_data = {'phone': phone_number, 'quote_status': 'confirmed', 'status': False}
        updating_quote = update_quote(quote_data)
        if updating_quote['status'] == 'ok':
            msg.body(responses('success_confirming_quote'))
            particular_customers.send_notification(updating_quote['id'])
        else:
            msg.body(responses('error_updating_quote'))
        return str(resp)
    if incoming_msg['Body'] == 'Cancelar':
        quote_data = {'phone': phone_number, 'quote_status': 'canceled', 'status': False}
        updating_quote = update_quote(quote_data)
        if updating_quote['status'] == 'ok':
            msg.body(responses('success_closing_quote'))
        else:
            msg.body(responses('error_updating_quote'))
        return str(resp)
    else:
        if location:
            if ('Latitude' in incoming_msg) and ('Longitude' in incoming_msg):
                response = bot_operations.calculate_cost_to_location(phone_number, location, incoming_msg, 'quoted')
                msg.body(response)
                responded = True
            if not responded:
                msg.body(responses('no_shipping_location'))
            return str(resp)
        else:
            result = particular_customers.particular_quote(phone_number, incoming_msg)
            msg.body(result)
            responded = True
            return str(resp)













