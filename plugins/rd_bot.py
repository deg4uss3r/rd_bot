from __future__ import unicode_literals
import requests
import json

outputs = []

def get_weather(city):
    APPID='181c98fe0d98b16f927103e0e0963ef5'
    OWM_URL ='http://api.openweathermap.org/data/2.5/weather?q='+city+'&units=imperial&APPID='+APPID
    
    r_block = requests.get(OWM_URL)
    r = r_block.json()
    temp = r['main']['temp']
    wind = r['wind']['speed']
    country = r['sys'['country']
    city_name = r['id']['name']

    response = " Current weather for " + city_name + ", " + country + str(temp) + " wind speed: " + str(wind)

    return response


def get_beers(pub):
    clientSecretFile = open(os.path.expanduser('~/Dropbox/private/untapped-private-api'), 'r') #have to use os.path.expanduser because of ~
    CLIENTSECRET=clientSecretFile.read()
    CLIENTID='189BD8671F3124A796C4B9C78BB8FED66DA4C4C9'
    

def process_message(data):
    #print(data) 
    channel = data['channel']

    try:
        content = data['text']
        user = '<@'+data['user']+'>'

    except:
        content = ''
        user = ''

    if channel == 'C1WFG1BS8' and '<@U2CEQ0RR6>' in content and 'get weather' in content:
        city = content[content.index('weather')+8:]
        output = user
        output += get_weather(city)
        outputs.append([channel, output]) 
