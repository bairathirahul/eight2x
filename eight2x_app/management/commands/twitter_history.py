from datetime import datetime
from pytz import utc
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db import Error

from eight2x_app.lib.geocode import get_country
from eight2x_app.lib.twitter_base import TwitterBase
from eight2x_app.models import Option, Status, User


class Command(BaseCommand, TwitterBase):
    help = 'Load Tweets history'
    
    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        TwitterBase.__init__(self)
    
    def handle(self, *args, **options):
        params = dict()
        params['query'] = ' OR '.join(settings.TWITTER_SEARCH_HASHTAGS)
        params['fromDate'] = '201709120000'
        params['maxResults'] = 100
        
        try:
            next_option = Option.objects.get(option_name='tweet_next_token')
            if len(next_option.option_value.strip()) > 0:
                params['next'] = next_option.option_value
        except ObjectDoesNotExist:
            next_option = Option(option_name='tweet_next_token', option_value='')
            next_option.save()
        
        while True:
            response = self.request('tweets/search/fullarchive/development.json', params)
            if response is not None:
                for s in response['results']:
                    try:
                        # find user
                        try:
                            user = User.objects.get(id=int(s['user']['id']))
                        except ObjectDoesNotExist:
                            user = User()
                            user.id = int(s['user']['id'])
                        
                        user.name = s['user']['name']
                        user.screen_name = s['user']['screen_name']
                        user.location = s['user']['location']
                        user.description = s['user']['description']
                        user.utc_offset = s['user']['utc_offset']
                        user.time_zone = s['user']['time_zone']
                        user.save()
                        
                        status = Status()
                        status.id = s['id']
                        status.created_at = utc.localize(datetime.strptime(s['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
                        status.text = s['text']
                        status.entities = []
                        if s['entities']['urls'] is not None:
                            for url in s['entities']['urls']:
                                status.entities.append(url['url'])
                        status.user = user
                        status.retweet_count = s['retweet_count']
                        status.favorite_count = s['favorite_count']
                        if s['geo'] is not None:
                            status.geo = s['geo']['coordinates']
                            status.country = get_country(status.geo[0], status.geo[1])
                        else:
                            status.geo = list()
                        status.lang = s['lang']
                        status.save()
                    except Error:
                        self.stderr('Error in inserting tweet ' + str(s['id']))
                
                print('Saved ' + str(len(response['results'])) + ' statuses')
                next_option.option_value = response['next']
                next_option.save()