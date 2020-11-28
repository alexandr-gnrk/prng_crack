import requests
import json

URL = 'http://95.217.177.249/casino'


def createacc(id_):
    url = URL + '/createacc'
    params = {'id': id_}
    r = requests.get(url, params)
    return r.json()


def play(mode, player, bet, num):
    url = URL + f'/play{mode}'
    params = {
        'id': player['id'],
        'bet': bet,
        'number': num
    }
    r = requests.get(url, params)
    return r.json()

