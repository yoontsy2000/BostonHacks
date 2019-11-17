from __future__ import print_function
from datetime import datetime, timedelta
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
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
    startT = datetime(2019, 11, 14, 0, 0)
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
    print(busys)

if __name__ == '__main__':
    main()