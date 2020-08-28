import requests
import json
from datetime import datetime
from datetime import time
from twilio.rest import Client
import time

#set variables for location of passing
latitude = 27.2038
longitude = -77.5011
altitude = 189
passes = 1

def checkToday(target_date, time):
    time_diff = datetime.timestamp(target_date) - datetime.timestamp(date.today())
    if time_diff < time and time_diff > 0:
        return True;
    else:
        return False

def get_risetime():
    response = requests.get("http://api.open-notify.org/iss-pass.json", params = {'lat':latitude, 'lon':longitude, 'alt':altitude, 'n':passes})
    response = json.loads(response.text)
    risetime = response['response'][0]['risetime']
    return risetime

def get_duration():
    response = requests.get("http://api.open-notify.org/iss-pass.json", params = {'lat':latitude, 'lon':longitude, 'alt':altitude, 'n':passes})
    response = json.loads(response.text)
    duration = response['response'][0]['duration']
    return duration

def send_message(message):
    message = client.messages.create(
                    body=message,
                    from_=from_number,
                    to=to_number
                )
    
def seconds_to_minutes(seconds):
    minutes = seconds // 60
    seconds %= 60
    return str(minutes) + " minutes and " + str(seconds) + " seconds"

risetime = get_risetime()
risetime = 1598597995
duration = get_duration()
duration_minutes = seconds_to_minutes(duration)
date = datetime.fromtimestamp(risetime)

account_sid = 'AC01719c32016ba6324d2684f4287edb3e'
auth_token = '0'
from_number = '+12029534316'
to_number = '+14692880626'
client = Client(account_sid, auth_token)

while True:
    if not checkToday(date, 3600):
        time.sleep(risetime - 3600 - datetime.timestamp(date.today()))
        send_message("The ISS will pass next in 1 hour")
    elif not checkToday(date, 300):
        time.sleep(risetime - 300 - datetime.timestamp(date.today()))
        send_message("The ISS will pass next in 5 minutes")
    else:
        time.sleep(risetime - datetime.timestamp(date.today()))
        send_message("The ISS is currently passing over your location. It will be passing for " + duration_minutes)
