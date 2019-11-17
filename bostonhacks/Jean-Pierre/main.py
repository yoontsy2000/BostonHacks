from twilio.rest import Client

account_sid = 'AC7fabac7430996e4dd2a0153bf0724e00'
auth_token = 'd4e73d92a84495e0734a6b4caa2a6d5d'
twilio_phone = '+12055489911'
receiver = '+18608064163'

client = Client(account_sid, auth_token)

message = client.messages.create(
    to= receiver,
    from_= twilio_phone,
    body='Bonjour, my name is Jean-Pierre. I am your Coi-ssistant!'
)

print(message.sid)
