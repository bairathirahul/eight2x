import re
from time import sleep

import nltk
from django.core.management.base import BaseCommand

from eight2x_app.models import Status, Option


class Command(BaseCommand):
    """
    Predict country of the tweets with country as empty
    """
    help = 'Predict Country of new tweets'
    
    def clean_tweet(self, tweet):
        """
        Clean the tweet from the useless information like Links, Mentions and RT tag
        :param tweet: Input tweet
        :return: cleaned tweet
        """
        tweet = re.sub(u'http\S+', u'', tweet)
        tweet = re.sub(u'(\s)@\w+', u'', tweet)
        tweet = re.sub(u'#', u'', tweet)
        tweet = tweet.replace(u'RT', u'')
        return tweet
    
    def handle(self, *args, **options):
        """
        Execute the command
        :param args: Command args
        :param options: Command options
        :return: Nothing
        """
        # Read list of countries
        countries = Option.objects.get(option_name='countries')
        tokenizer = nltk.TweetTokenizer()
        
        # Read countries and prepare training dataset
        training_dataset = []
        for country in countries.option_value:
            if country is None:
                continue
            
            # Extract training words specific to each country
            status_words = list()
            statuses = Status.objects.filter(country=country)[:100]
            for status in statuses:
                status.text = self.clean_tweet(status.text)
                status_words.extend(tokenizer.tokenize(status.text))
            
            status_words = dict((word, True) for word in status_words)
            training_dataset.append((status_words, country))
        
        # Train the Naive Bayes classifier
        classifier = nltk.NaiveBayesClassifier.train(training_dataset)
        
        # Read status without countries
        while True:
            statuses = Status.objects.filter(country='')[:500]
            for status in statuses:
                status.text = self.clean_tweet(status.text)
                status_words = tokenizer.tokenize(status.text)
                status_words = dict((word, True) for word in status_words)
                # Predict country using the trained model
                country = classifier.classify(status_words)
                if country is not None:
                    status.country = country
                    status.predicted_country = True
                    status.save()
            sleep(5)
