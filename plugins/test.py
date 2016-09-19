import requests
import json




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
        beer_sentence = str(i['beer']['beer_name'] + " by " + i['brewery']['brewery_name'] + " a " + i['beer']['beer_style'] + " at " + i['venue']['venue_name'])
        if beer_sentence in beer_return_list:
            print("skipped")
            continue
        else:
            print("added")
            beer_return_list.append(beer_sentence)
    print(beer_return_list)

if __name__ == '__main__':
    get_beers()
