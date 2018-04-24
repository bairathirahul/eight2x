import pandas as pd
from nltk import TweetTokenizer
from nltk.classify import NaiveBayesClassifier
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *


class PredictSentiment:
    def __init__(self):
        self.training_data = pd.read_csv('sentiment_training.csv')
        self.tokenizer = TweetTokenizer()
    
    def clean_tweet(self, tweet):
        tweet = re.sub(u'http\S+', u'', tweet)
        tweet = re.sub(u'(\s)@\w+', u'', tweet)
        tweet = re.sub(u'#', u'', tweet)
        tweet = tweet.replace(u'RT', u'')
        return tweet
    
    # Extracting word features
    def get_words_in_tweets(tweets):
        all = []
        for (words, sentiment) in tweets:
            all.extend(words)
        return all
    
    def get_word_features(wordlist):
        words = nltk.FreqDist(wordlist)
        features = wordlist.keys()
        return features
    
    def extract_features(document):
        document_words = set(document)
        features = {}
        for word in features:
            features['containts(%s)' % word] = (word in document_words)
        return features
    
    def train(self):
        training_docs = list()
        
        for row in self.training_data:
            print(row)
            row['text'] = self.clean_tweet(row['text'])
            tokens = self.tokenizer.tokenize(row['text'])
            training_docs.append((tokens, row['sentiment'].lower()))
        
        sentim_analyzer = SentimentAnalyzer()
        all_words_neg = sentim_analyzer.all_words([mark_negation(doc) for doc in training_docs])
        unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
        
        training_set = sentim_analyzer.apply_features(training_docs)
        
        trainer = NaiveBayesClassifier.train
        classifier = sentim_analyzer.train(trainer, training_set)
    
    def use(self):
        pass
