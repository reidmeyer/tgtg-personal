#!/usr/bin/env python3
import os
import time as sleeptime
from datetime import datetime, time
from tgtg import TgtgClient
from pushover import init, Client

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time


pushover_token = os.getenv("PUSHOVER_TOKEN")
init(pushover_token)
client = TgtgClient(email=os.getenv("EMAIL"))
credentials = client.get_credentials()

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

            items = newClient.get_items(page_size=100)

            for item in items:
                if item['items_available']>0:
                    if item['item']['item_id'] not in items_notified:
                        print('notify')
                        print(item)
                        message = f"{item['store']['store_name']} has sushi"
                        Client(os.getenv("PUSHOVER_CLIENT")).send_message(message, title="SUSHI")

                    items_notified.append(item['item']['item_id'])

            sleeptime.sleep(60)

    except Exception as e:
        print(e)
        print("trying again")
        sleeptime.sleep(60)
