import os
from twilio.rest import Client

# api account stuff
account_sid = 'AC7fabac7430996e4dd2a0153bf0724e00'
auth_token = 'd4e73d92a84495e0734a6b4caa2a6d5d'
twilio_phone = '+12132124786'


# receiver phone number
receiver = '+18608064163'

# sets up the client
client = Client(account_sid, auth_token)

# creates a message
message = client.messages.create(
    to= receiver,
    from_= twilio_phone,
    body='Bonjour, my name is Jean-Pierre. I am your Coi-ssistant!'
)

# sends the message to the client
print(message.sid)
