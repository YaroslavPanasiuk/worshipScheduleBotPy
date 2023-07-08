from __future__ import print_function
import os
import time

import telebot
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1wM3M_WVf7YtEfSar1dZ2-2cQPY3iA8V4cSGjJnmJbmY"
SAMPLE_RANGE_NAME = "розклад!A1:C10000"


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[2]))
    except HttpError as err:
        print(err)


def get_next_days(date, count):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

    except HttpError as err:
        print(err)
    output = ""
    for i in range(len(values)):
        if values[i][0] == date:
            for j in range(count):
                output += '%s %s %s\n' % (values[i+j][0], values[i+j][1], values[i+j][2])
    return output


def next_monday(date):
    days_to_monday = 7 - date.weekday()
    result = date + datetime.timedelta(days=days_to_monday)
    return result


if __name__ == '__main__':
    date = datetime.date(2023, 7, 10)
    BOT_TOKEN = '6334981753:AAFADpyUu-qupi7SCxtIjpRM8ZKjuximVPw'
    bot = telebot.TeleBot(BOT_TOKEN)
    time_to_send_message = datetime.datetime(next_monday(datetime.date.today()).year,
                                             next_monday(datetime.date.today()).month,
                                             next_monday(datetime.date.today()).day, 10)
    print(time_to_send_message)
    while True:
        bot.send_message(388098248, get_next_days(time_to_send_message.strftime("%d.%m.%Y"), 7))
        if datetime.datetime.now() > time_to_send_message:
            bot.send_message(388098248, get_next_days(time_to_send_message.strftime("%d.%m.%Y"), 7))
            time_to_send_message = datetime.datetime(next_monday(datetime.date.today()).year,
                                                     next_monday(datetime.date.today()).month,
                                                     next_monday(datetime.date.today()).day, 10)
        time.sleep(360)


