"""
    Project: 82x
    Authors: Rahul Bairathi, Nipun Gupta, Rajendra Jadi
"""
import json

import requests
from django.conf import settings
from requests.exceptions import HTTPError, ConnectionError


def get_country(lat, lng):
    """
    Get country from latitude and longitude information using Google Reverse Geocode api
    :param lat: Latitute
    :param lng: Longitude
    :return: Country ISO Code
    """
    
    # Setup the query
    query = dict(latlng=str(lat) + ',' + str(lng), key=settings.GOOGLE_API_KEY)
    geo_api_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    try:
        # Read the response
        response = requests.get(geo_api_url, params=query)
        if response.status_code == 200:
            response = json.loads(response.text)
            if response['status'] == 'OK':
                components = response['results'][0]['address_components']
                for c in components:
                    if c['types'][0] == 'country':
                        return c['short_name'].lower()
    except (ConnectionError, HTTPError) as e:
        print('Error: Connection error while Geocoding - ' + str(e))
    
    return None
