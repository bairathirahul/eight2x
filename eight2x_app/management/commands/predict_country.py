import re

import nltk
from django.core.management.base import BaseCommand

from eight2x_app.models import Status, Option


class Command(BaseCommand):
    help = 'Predict Country of new tweets'
    
    def clean_tweet(self, tweet):
        tweet = re.sub(u'http\S+', u'', tweet)
        tweet = re.sub(u'(\s)@\w+', u'', tweet)
        tweet = re.sub(u'#', u'', tweet)
        tweet = tweet.replace(u'RT', u'')
        return tweet
    
    def handle(self, *args, **options):
        # Read list of countries
        countries = Option.objects.get(option_name='countries')
        tokenizer = nltk.TweetTokenizer()
        
        # Read countries and prepare training dataset
        training_dataset = []
        for country in countries.option_value:
            if country is None:
                continue
                
            status_words = list()
            statuses = Status.objects.filter(country=country)[:5]
            for status in statuses:
                status.text = self.clean_tweet(status.text)
                status_words.extend(tokenizer.tokenize(status.text))
                
            status_words = dict((word, True) for word in status_words)
            training_dataset.append((status_words, country))
        
        classifier = nltk.NaiveBayesClassifier.train(training_dataset)
        
        # Read status without countries
        statuses = Status.objects.filter(country='')[:5]
        for status in statuses:
            status.text = self.clean_tweet(status.text)
            status_words = tokenizer.tokenize(status.text)
            status_words = dict((word, True) for word in status_words)
            country = classifier.classify(status_words)
            print(country)
