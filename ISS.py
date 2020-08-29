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

#checks if the current time is within @param time seconds of the target_date
def checkToday(target_date, time):
    time_diff = datetime.timestamp(target_date) - datetime.timestamp(date.today())
    return True if time_diff < time else False

#makes a call to return the risetime of the next ISS passing
def get_risetime():
    response = requests.get("http://api.open-notify.org/iss-pass.json", params = {'lat':latitude, 'lon':longitude, 'alt':altitude, 'n':passes})
    response = json.loads(response.text)
    risetime = response['response'][0]['risetime']
    #if (risetime < datetime.timestamp(datetime.today())):
        #risetime += 12*60*60
    return risetime

#makes a call to return the duration of the next ISS passing
def get_duration():
    response = requests.get("http://api.open-notify.org/iss-pass.json", params = {'lat':latitude, 'lon':longitude, 'alt':altitude, 'n':passes})
    response = json.loads(response.text)
    duration = response['response'][0]['duration']
    return duration

#uses twilio client to create and send a message to the to_number
def send_message(message):
    message = client.messages.create(
                    body=message,
                    from_=from_number,
                    to=to_number
                )

#returns string of minutes and seconds given a number of seconds
def seconds_to_minutes(seconds):
    minutes = seconds // 60
    seconds %= 60
    return str(minutes) + " minutes and " + str(seconds) + " seconds"

#waits until 1 hour and 5 minutes before the passing and sends messages as reminders
#as well as a message when it is currently passing
def send_notifications(date, risetime, duration_minutes):
    if not checkToday(date, 3600):
        time.sleep(risetime - 3600 - datetime.timestamp(date.today()))
        send_message("The ISS will pass next in 1 hour")
    elif not checkToday(date, 300):
        time.sleep(risetime - 300 - datetime.timestamp(date.today()))
        send_message("The ISS will pass next in 5 minutes")
    else:
        time.sleep(risetime - datetime.timestamp(date.today()))
        send_message("The ISS is currently passing over your location. It will be passing for " + duration_minutes)

#Create twilio client with sid and auth_token
account_sid = 'AC01719c32016ba6324d2684f4287edb3e'
auth_token = '<Auth_Token>'
from_number = '+12029534316'
to_number = '+14692880626'
client = Client(account_sid, auth_token)

#Send 
while True:
    #get risetime and duration from api
    risetime = get_risetime()
    duration = get_duration()
    #convert the duration to minutes and seconds for readability
    duration_minutes = seconds_to_minutes(duration)
    #convert the risetime in seconds to a datetime object
    date = datetime.fromtimestamp(risetime)
    #start sending notification messages for the next passing
    send_notifications(date, risetime, duration_minutes)
    #wait 5 seconds so it doesn't check the same passing twice
    #and repeat a message notification
    time.sleep(5)
