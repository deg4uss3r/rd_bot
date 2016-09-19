from __future__ import unicode_literals
import requests
import json
import os
import sys

outputs = []

def get_lat_lng(city):
    try:
        googleclientSecretFile = open('google_api_key', 'r')
        GCLIENTSECRET = googleclientSecretFile.read()
        GCLIENTSECRET = GCLIENTSECRET[:-1]
    except:
        print("fatal error reading google API key")
        sys.exit(1)

    addr = city.split(' ')
    address=''

    for i in addr:
        address+=i
        address+='+'
    
    try:
        google_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + address + '&key=' + GCLIENTSECRET
        g_block = requests.get(google_url)
        g = g_block.json()
    except:
        print("fatal error with google maps request")
        sys.exit(1)

    g_lat = g['results'][0]['geometry']['location']['lat']
    g_lng = g['results'][0]['geometry']['location']['lng']

    return g_lat, g_lng

def get_weather(city):
    lat,lng = get_lat_lng(city)
    APPID = '181c98fe0d98b16f927103e0e0963ef5'
    OWM_URL = 'http://api.openweathermap.org/data/2.5/weather?&lat=' + str(lat) + '&lon=' + str(lng) + '&units=imperial&APPID='+APPID
    
    try:
        r_block = requests.get(OWM_URL)
        r = r_block.json()
    except:
        print("fatal error with Open Weather Request")
        sys.exit(1)

    temp = r['main']['temp']
    country = r['sys']['country']
    city_name = r['name']

    response = " Current weather for " + city_name + ", " + country + " " + str(temp)
    return response

def get_beers(city):
    try:
        clientSecretFile = open('untapped-private-api', 'r')
        CLIENTSECRET = clientSecretFile.read()
        CLIENTSECRET = CLIENTSECRET[:-1]
    except:
        print("fatal error reading untappd API key")
        sys.exit(1)

    lat,lng = get_lat_lng(city)
    

    try:
        UNTAPPD = 'https://api.untappd.com/v4/thepub/local/?&client_id=189BD8671F3124A796C4B9C78BB8FED66DA4C4C9&client_secret='+CLIENTSECRET+'&radius=2&lat=' + str(lat) + '&lng=' + str(lng)
    
    except:
        print("fatal error with untappd request")
        sys.ext(1)
    try:
        b_block = requests.get(UNTAPPD)
        b = b_block.json()
        beer_list = b['response']['checkins']['items']
    except:
        print("fatal error with parsing untappd response")
        sys.exit(1)

    beer_return_list = []
    beer_exists_flag = False

    for i in beer_list:
        beer_sentence = "* " + i['beer']['beer_name'] + " (" +  i['beer']['beer_style'] + ") by " + i['brewery']['brewery_name'] + " at " + i['venue']['venue_name'] 
        beer_sentence.encode('UTF-8')
        beer_name = i['beer']['beer_name']
        beer_name.encode('UTF-8')
        
        for b in beer_return_list:
            if beer_name in b:
                beer_exists_flag = True
            else:
                beer_exists_flag = False
    
        if beer_exists_flag:
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
        outputs.append([channel, "sorry " + user + "something went really wrong"])
        print("fatal error parsing slack input")
        sys.exit(1)

    content = content.lower()

    if content[:12] == '<@u2ceq0rr6>' and 'get weather' in content:
        city = content[content.index('weather')+8:]
        output = user
        output += get_weather(city)
        outputs.append([channel, output])

    if content[:12] == '<@u2ceq0rr6>' and 'get beer' in content:
        city = content[content.index('beer')+5:]
        beer_list = get_beers(city)
        output = user+'\n'
        for i in beer_list:
            output += i+'\n'

        outputs.append([channel, output])
