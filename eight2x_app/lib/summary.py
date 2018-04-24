"""
    Project: 82x
    Authors: Rahul Bairathi, Nipun Gupta, Rajendra Jadi
"""
from collections import defaultdict
from heapq import nlargest
from string import punctuation

from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer


class FrequencySummarizer:
    """
    Generate a summary of the provided tweets
    """
    def __init__(self, min_cut=0.1, max_cut=0.9):
        """
         Initilize the text summarizer.
         Words that have a frequency term lower than min_cut
         or higer than max_cut will be ignored.
        """
        self._min_cut = min_cut
        self._max_cut = max_cut
        self._stopwords = set(stopwords.words('english') + list(punctuation))
        self._tokenizer = TweetTokenizer()
    
    def _compute_frequencies(self, word_sent):
        """
          Compute the frequency of each of word.
          Input:
           word_sent, a list of sentences already tokenized.
          Output:
           freq, a dictionary where freq[w] is the frequency of w.
        """
        freq = defaultdict(int)
        for s in word_sent:
            for word in s:
                if word not in self._stopwords:
                    freq[word] += 1
        # frequencies normalization and fitering
        m = float(max(freq.values()))
        keys_to_delete = list()
        for w in freq.keys():
            freq[w] = freq[w] / m
            if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
                keys_to_delete.append(w)
        
        for key in keys_to_delete:
            del freq[key]
        return freq
    
    def summarize(self, sents, n):
        """
          Return a list of n sentences
          which represent the summary of text.
        """
        assert n <= len(sents)
        word_sent = [self._tokenizer.tokenize(s.lower()) for s in sents]
        self._freq = self._compute_frequencies(word_sent)
        ranking = defaultdict(int)
        for i, sent in enumerate(word_sent):
            for w in sent:
                if w in self._freq:
                    ranking[i] += self._freq[w]
        sents_idx = self._rank(ranking, n)
        return [sents[j] for j in sents_idx]
    
    def _rank(self, ranking, n):
        """ return the first n sentences with highest ranking """
        return nlargest(n, ranking, key=ranking.get)
