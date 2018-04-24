from eight2x_app.models import Status
import nltk
from nltk.tokenize import TweetTokenizer
from nltk import pos_tag, ne_chunk
from nltk.tree import Tree
from nltk.tag.stanford import StanfordNERTagger

import inspect

from textacy.vsm import Vectorizer
import textacy.vsm

import scipy.sparse as sp

from tqdm import *

import re

def clean_tweets(tweet):
    tweet = re.sub(u'http\S+', u'', tweet)
    tweet = re.sub(u'(\s)@\w+', u'', tweet)
    tweet = re.sub(u'#', u'', tweet)
    tweet = tweet.replace(u'RT', u'')
    return tweet

def generate_summary(statuses):
    status_tokens = list()
    tokenizer = TweetTokenizer()
    
    for status in statuses:
        status.text = clean_tweets(status.text)
        status_tokens.append(tokenizer.tokenize(status.text))
        
        
    pass
