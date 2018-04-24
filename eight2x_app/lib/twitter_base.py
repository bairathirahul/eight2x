"""
    Project: 82x
    Authors: Rahul Bairathi, Nipun Gupta, Rajendra Jadi
"""
import json
from urllib.parse import urlencode

import requests
from django.conf import settings
from requests.exceptions import HTTPError, ConnectionError

class TwitterBase:
    """
    Base class to read twitter information
    """
    TWITTER_URL = 'https://api.twitter.com/'
    TWITTER_API_VERSION = '1.1/'
    
    def __init__(self):
        """
        Performs authentication using OAuth2
        """
        request_url = TwitterBase.TWITTER_URL + 'oauth2/token'
        
        try:
            auth = (settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
            headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
            data = 'grant_type=client_credentials'
            response = requests.post(request_url, data=data, auth=auth, headers=headers)
            
            if response.status_code == 200:
                response = json.loads(response.text)
                if response['token_type'] == 'bearer':
                    self.access_token = response['access_token']
                    return
            else:
                response.raise_for_status()
        except (ConnectionError, HTTPError) as e:
            print('Error: generating bearer token - ' + str(e))
    
    def request(self, endpoint, params):
        """
        Send request to the specificed endpoint
        :param endpoint: Endpoint name
        :param params: parameters
        :return: Tweets
        """
        request_url = TwitterBase.TWITTER_URL + TwitterBase.TWITTER_API_VERSION + endpoint
        query = urlencode(params)
        
        try:
            headers = {'Authorization': 'Bearer ' + self.access_token}
            response = requests.get(request_url + '?' + query, headers=headers)
            if response.status_code == 200:
                response = json.loads(response.text)
                return response
            else:
                response.raise_for_status()
        except (ConnectionError, HTTPError) as e:
            print('Error: Connection error while requesting with query - ' + query + ' - ' + str(e))
        
        return None
