# Google API includes
from __future__ import print_function
from datetime import datetime, timedelta
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# Twilio includes
from flask import Flask, request, redirect, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

# ----- Twilio API Code ----- #

app = Flask(__name__)

# api account stuff
account_sid = 'AC7fabac7430996e4dd2a0153bf0724e00'
auth_token = 'd4e73d92a84495e0734a6b4caa2a6d5d'
twilio_phone = '+12132124786'

# receiver phone number
receiver = '+18608064163' # should be configurabe from front end

# sets up the client
client = Client(account_sid, auth_token)

# creates a motivational message based on your activity list
# def create_message(message):
#     message = 'Bonjour, my name is Jean-Pierre. I am your Croi-ssistant!'
#     return message

# sends the message
def send_message(msg):
    message = client.messages.create(
        to= receiver,
        from_= twilio_phone,
        body=msg
    )
    print(message.sid)


# ----- Google Calender API ----- #

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def google_calendar():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    result = service.calendarList().list().execute()
    calendar_ids = []
    for i in range(len(result['items'])):
       calendar_ids.append(result['items'][i]['id'])
    startT = datetime.today()
    endT = startT + timedelta(hours=24)
    query_body = {
           "timeMin": startT.strftime("%Y-%m-%dT%H:%M:%S"+"Z"),
           "timeMax": endT.strftime("%Y-%m-%dT%H:%M:%S"+"Z"),
           'items': result['items']
    }
    
    query_result = service.freebusy().query(body=query_body).execute()
    busys = []
    for i in range(len(calendar_ids)):
        busys.append(query_result['calendars'][calendar_ids[i]]['busy'])
    print("\n" + str(get_freetime(busys, '2019-11-17T08:00:00Z', '2019-11-17T22:00:00Z')) + "\n")


def get_freetime(busys, begin_day, end_day):
    # beginning_time = '2019-11-17T08:00:00Z'
    # finish_time = '2019-11-17T22:00:00Z'
    final_time_list = extract_time(busys)
    time_list = []
    if begin_day <= final_time_list[0]:
        time_list.append(begin_day)
    for i in range(len(final_time_list)-1):
        if i % 2 == 0:
            start_block = final_time_list[i]
            end_block = final_time_list[i+1]
            if begin_day <= start_block:
                time_list.append(start_block)
            if end_day >= end_block: 
                time_list.append(end_block)
    if end_day >= final_time_list[len(final_time_list)-1]:
        time_list.append(end_day)

    # print('time list is')
    # print(time_list)
    free_times = []
    while len(time_list) > 1:
        free_period = {'start': time_list[0], 'end': time_list[1]}
        free_times.append(free_period)
        time_list = time_list[2:]
    # last_period = {'start': time_list[0], 'end': end_day}
    # free_times.append(last_period)
    return free_times


def extract_time(list):
    array = []
    for i in list:
        for event in i:
            event_start = event['start']
            event_end = event['end']
            array.append(event_start)
            array.append(event_end)
    return array

introduction = False

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    global introduction
    resp = MessagingResponse()
    resp.message("Oui oui, Jean-Pierre received your message!")
    send_message('I noticed that you went to the gym three times this week, but you still havent mediated like you wanted to.')
    send_message('It looks like that you have some free time this afternoon from 2:30PM to 4:00PM. Would that be a good time to meditate?')
    if introduction != True:
        send_message('Hello, my name is Jean Pierre, your Croissistant!')
        introduction = True
    google_calendar()
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)