import os
from twilio.rest import Client
from flask import Flask, request, jsonify, render_template, url_for, redirect
import requests

# api account stuff
account_sid = 'AC7fabac7430996e4dd2a0153bf0724e00'
auth_token = 'd4e73d92a84495e0734a6b4caa2a6d5d'
twilio_phone = '+12132124786'


# receiver phone number
receiver = request.form['phone_number']

# sets up the client
client = Client(account_sid, auth_token)


def create_message(activity_list):
    message = 'Bonjour, my name is Jean-Pierre. I am your Coi-ssistant!'
    return message

# creates a message
message = client.messages.create(
    to= receiver,
    from_= twilio_phone,
    body=create_message(activity_list)
)

# sends the message to the client
print(message.sid)
