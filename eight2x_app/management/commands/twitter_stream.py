import tweepy
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db import Error
from pytz import utc

from eight2x_app.lib.geocode import get_country
from eight2x_app.models import Status, User


class Command(BaseCommand):
    help = 'Load Tweets history'
    
    def handle(self, *args, **options):
        auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_TOKEN_SECRET)
        
        api = tweepy.API(auth)
        listener = TweetListener()
        stream = tweepy.Stream(auth=api.auth, listener=listener)
        stream.filter(track=settings.TWITTER_SEARCH_HASHTAGS)


class TweetListener(tweepy.StreamListener):
    def on_status(self, s):
        try:
            # find user
            try:
                user = User.objects.get(id=int(s.author.id))
            except ObjectDoesNotExist:
                user = User()
                user.id = s.author.id
            
            user.name = s.author.name
            user.screen_name = s.author.screen_name
            user.location = s.user.location
            user.description = s.user.description
            user.utc_offset = s.user.utc_offset
            user.time_zone = s.author.time_zone
            user.lang = s.author.lang
            user.save()
            
            status = Status()
            status.id = s.id
            status.created_at = utc.localize(s.created_at)
            status.text = s.text
            status.entities = []
            if s.entities['urls'] is not None:
                for url in s.entities['urls']:
                    status.entities.append(url['url'])
            status.user = user
            status.retweet_count = s.retweet_count
            status.favorite_count = s.favorite_count
            if s.geo is not None:
                status.geo = s.geo['coordinates']
                status.country = get_country(status.geo[0], status.geo[1])
            else:
                status.geo = list()
            status.lang = s.lang
            status.predicted_country = False
            status.sentiment = ''
            status.labels = []
            status.save()
            print('Inserted tweet with ID ' + str(s.id))
        except Error:
            print('Error in inserting tweet ' + str(s['id']))
