"""
    Project: 82x
    Authors: Rahul Bairathi, Nipun Gupta, Rajendra Jadi
"""
import os
from time import sleep

import pandas as pd
from django.core.management.base import BaseCommand
from nltk import TweetTokenizer
from nltk.corpus import stopwords
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.stem.porter import *
import string

import eight2x_app
from eight2x_app.models import Status


class Command(BaseCommand):
    help = 'Predict sentiment of tweets'
    
    def __init__(self):
        super(Command, self).__init__()
        app_path = os.path.dirname(eight2x_app.__file__)
        dataset_path = os.path.join(os.path.sep, app_path, 'dataset', 'sentiment_training.csv')
        self.training_data = pd.read_csv(dataset_path)
        self.tokenizer = TweetTokenizer()
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.translate_table = dict((ord(char), None) for char in string.punctuation)
    
    def clean_tweet(self, tweet):
        tweet = re.sub(u'http\S+', u'', tweet)
        tweet = re.sub(u'(\s)@\w+', u'', tweet)
        tweet = re.sub(u'#', u'', tweet)
        tweet = tweet.replace(u'RT', u'')
        return tweet
    
    # Extracting word features
    def get_words_in_tweets(self, tweets):
        all = []
        for (words, sentiment) in tweets:
            all.extend(words)
        return all
    
    def get_word_features(self, wordlist):
        """
        Extract word features from the training dictionary
        :param wordlist:
        :return:
        """
        words = nltk.FreqDist(wordlist)
        features = wordlist.keys()
        return features
    
    def extract_features(self, document_words):
        document_words = [token.lower() for token in document_words if not token in self.stop_words]
        document_words = [self.stemmer.stem(token) for token in document_words]
        document_words = set(document_words)
        features = {}
        for word in document_words:
            features[word] = (word in document_words)
        return features
    
    def train(self):
        training_docs = list()
        
        for index, row in self.training_data.iterrows():
            row['text'] = self.clean_tweet(row['text'])
            row['text'] = row['text'].translate(self.translate_table)
            tokens = self.tokenizer.tokenize(row['text'])
            training_docs.append((tokens, row['sentiment'].lower()))
        
        sentim_analyzer = SentimentAnalyzer()
        training_set = nltk.classify.apply_features(self.extract_features, training_docs)
        self.classifier = nltk.NaiveBayesClassifier.train(training_set)
    
    def use(self):
        # Read status without countries
        while True:
            statuses = Status.objects.filter(sentiment='')[:100]
            for status in statuses:
                status.text = self.clean_tweet(status.text)
                status.text = status.text.translate(self.translate_table)
                tokens = self.tokenizer.tokenize(status.text)
                sentiment = self.classifier.classify(self.extract_features(tokens))
                if sentiment is not None:
                    status.sentiment = sentiment
                    status.save()
            sleep(5)
    
    def handle(self, *args, **options):
        self.train()
        self.use()
