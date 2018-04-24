"""
    Project: 82x
    Authors: Rahul Bairathi, Nipun Gupta, Rajendra Jadi
"""
import re
from time import sleep

import nltk
from django.core.management.base import BaseCommand

from eight2x_app.models import Status, Option


class Command(BaseCommand):
    """
    Predict country of the tweets with country as empty
    """
    help = 'Predict Labels of new tweets'
    
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
        labels = Option.objects.get(option_name='labels')
        tokenizer = nltk.TweetTokenizer()
        
        # Read tweet labels and prepare training dataset
        training_dataset = []
        for label in labels.option_value:
            if label is None:
                continue
            
            # Extract training words specific to each label
            status_words = list()
            statuses = Status.objects.filter(country=label)[:100]
            for status in statuses:
                status.text = self.clean_tweet(status.text)
                status_words.extend(tokenizer.tokenize(status.text))
            
            status_words = dict((word, True) for word in status_words)
            training_dataset.append((status_words, label))
        
        # Train the Naive Bayes classifier
        classifier = nltk.NaiveBayesClassifier.train(training_dataset)
        
        # Read status without labels
        while True:
            statuses = Status.objects.filter(country='')[:500]
            for status in statuses:
                status.text = self.clean_tweet(status.text)
                status_words = tokenizer.tokenize(status.text)
                status_words = dict((word, True) for word in status_words)
                # Predict label using the trained model
                label = classifier.classify(status_words)
                if label is not None:
                    status.label = label
                    status.predicted_country = True
                    status.save()
            sleep(5)
