#!/usr/bin/env python3
import os
import time as sleeptime
from datetime import datetime, time
from typing import Dict
from tgtg import TgtgClient
import requests

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def notify(message):
    url = 'https://ntfy.sh/reid-02-17-2024'
    response = requests.post(url, data=message.encode(encoding='utf-8'))

    if response.status_code == 200:
        print(f"Message sent successfully: {message}")
    else:
        print(f"Error sending message: {response.text}")

first_time = True

client: TgtgClient
credentials: Dict


while True:
    try:
        if first_time or is_time_between(time(8,00), time(23,30)):
            first_time = False
            notify("check email")
            client = TgtgClient(email=os.getenv("EMAIL"))
            credentials = client.get_credentials()
            break
        else:
            print("Sleeping since you aren't awake")
            sleeptime.sleep(60*60)
    except Exception as e:
        print(f"Sleeping since you didn't respond to confirmation email {e}")
        sleeptime.sleep(60*60)


items_notified = []
while True:
    try:
        newClient = TgtgClient(access_token=credentials['access_token'], refresh_token=credentials['refresh_token'], cookie=credentials['cookie'], user_id=credentials['user_id'])

        # run every minute
        while True:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Starting Current Time =", current_time)

            # if time is between 1:30-1:30am
            if is_time_between(time(3,00), time(3,10)):
                    items_notified = []
                    open('log.txt', 'w').close()
                    sleeptime.sleep(20*60)
                    continue

            items = newClient.get_items(page_size=100)

            for item in items:
                if item['items_available']>0:
                    if item['item']['item_id'] not in items_notified:
                        if is_time_between(time(8,00), time(23,30)):
                            print('notify')
                            print(item)
                            notify(f"Store: {item['store']['store_name']}")
                            items_notified.append(item['item']['item_id'])

            sleeptime.sleep(60)

    except Exception as e:
        print(e)
        print("trying again")
        sleeptime.sleep(60)
