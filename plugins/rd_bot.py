from __future__ import unicode_literals
import requests
import json
import os

outputs = []

def get_weather(city):
    APPID = '181c98fe0d98b16f927103e0e0963ef5'
    OWM_URL = 'http://api.openweathermap.org/data/2.5/weather?q='+city+'&units=imperial&APPID='+APPID
     
    r_block = requests.get(OWM_URL)
    
    r = r_block.json()
    temp = r['main']['temp']
    wind = r['wind']['speed']
    country = r['sys']['country']
    city_name = r['name']

    response = " Current weather for " + city_name + ", " + country + " " + str(temp)
    return response

def get_beers():
    clientSecretFile = open('untapped-private-api', 'r')
    CLIENTSECRET = clientSecretFile.read()
    CLIENTSECRET = CLIENTSECRET[:-1]
    UNTAPPD = 'https://api.untappd.com/v4/thepub/local/?&client_id=189BD8671F3124A796C4B9C78BB8FED66DA4C4C9&client_secret='+CLIENTSECRET+'&lat=53.9986&lng=-1.538'
    b_block = requests.get(UNTAPPD)
    b = b_block.json()
    beer_list = b['response']['checkins']['items']
    beer_return_list = []

    for i in beer_list:
        beer_sentence = i['beer']['beer_name'] + " by " + i['brewery']['brewery_name'] + " a " + i['beer']['beer_style'] + " at " + i['venue']['venue_name']
        beer_sentence.encode('UTF-8')

        if beer_sentence in beer_return_list:
            continue
        else:
            beer_return_list.append(beer_sentence)

    return beer_return_list


def process_message(data):
    channel = data['channel']

    try:
        content = data['text']
        user = '<@'+data['user']+'>'

    except:
        content = ''
        user = ''

    if content[:12] == '<@U2CEQ0RR6>' and 'get weather' in content:
        city = content[content.index('weather')+8:]
        output = user
        output += get_weather(city)
        outputs.append([channel, output])

    if content[:12] == '<@U2CEQ0RR6>' and 'get beer' in content:
        beer_list = get_beers()
        output = user+'\n'
        for i in beer_list:
            output += i+'\n'

        outputs.append([channel, output])
