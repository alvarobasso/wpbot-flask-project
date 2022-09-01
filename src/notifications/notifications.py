# Download the helper library from https://www.twilio.com/docs/python/install
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

def send_whats_app_notification( recipient_phone_number:int, message:str):
    message = client.messages \
        .create(
            #media_url=['https://images.unsplash.com/photo-1545093149-618ce3bcf49d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80'],
            body=message,
            from_='whatsapp:+14155238886',
            to='whatsapp:'+recipient_phone_number
        )
    return message.sid

def send_whats_app_location( recipient_phone_number:int, message:str, location:str):
    message = client.messages \
        .create(
            body=location,
            persistent_action=['geo:'+location+'|'+message],
            from_='whatsapp:+14155238886',
            to='whatsapp:'+recipient_phone_number
        )
    return message.sid
