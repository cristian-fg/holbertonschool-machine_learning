#!/usr/bin/env python3
"""home planets of all sentient species"""
import requests


def do_request(url):
    """function that do request
    Args:
    -> url: to process

    Return:
    -> json object
    """
    response = requests.get(url)
    return response.json()


def sentientPlanets():
    """names of the home planets
    of all sentient species.

    Return:
    -> names of the home planets
    """
    names = []
    url = 'https://swapi-api.hbtn.io/api/species/'
    try:
        res_j = do_request(url)

        while(True):
            for obj in res_j['results']:
                if obj['designation'] == 'sentient':
                    if obj['homeworld'] is not None:
                        new_r = do_request(obj['homeworld'])
                        names.append(new_r['name'])

            if res_j['next'] is None:
                return names

            if res_j['next'] is not None:
                res_j = do_request(res_j['next'])

    except Exception:
        return names