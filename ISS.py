import requests
import json
from datetime import datetime
from datetime import time
from twilio.rest import Client

def checkTime(target_date):
    if (date.today != target_date)

#set variables for location of passing
latitude = 27.2038
longitude = -77.5011
altitude = 189
passes = 1

response = requests.get("http://api.open-notify.org/iss-pass.json", params = {'lat':latitude, 'lon':longitude, 'alt':altitude, 'n':passes})
response = json.loads(response.text)
risetime = response['response'][0]['risetime']

date = datetime.fromtimestamp(risetime)

account_sid = 'AC01719c32016ba6324d2684f4287edb3e'
auth_token = '580d6ec5993b9f596dcdfbc88a22409f'
from_number = '+12029534316'
to_number = '+14692880626'
client = Client(account_sid, auth_token)

message = client.messages.create(
                     body="The ISS will pass next on " + date.strftime("%A, %B %d, %Y ") + "at " + date.strftime("%I:%M"),
                     from_=from_number,
                     to=to_number
                 )